import { AutoRouter } from 'itty-router';
import {
  InteractionResponseType,
  InteractionType,
  InteractionResponseFlags,
  verifyKey,
} from 'discord-interactions';
import {
  HOUSE_GROUP_COMMAND,
  USER_GROUP_COMMAND,
} from './commands.js';
import Household from './household';

class JsonResponse extends Response {
  constructor(body, init) {
    const jsonBody = JSON.stringify(body);
    init = init || {
      headers: {
        'Content-Type': 'application/json;charset=UTF=8',
      },
    };
    super(jsonBody, init);
  }
}

const router = AutoRouter();

function hasAdminPermissions(member) {
  return member.permissions & (1 << 3); // ADMINISTRATOR permission bitfield is 1 << 3
}

function getNoAdminWarning() {
  return new JsonResponse({
    type: InteractionResponseType.CHANNEL_MESSAGE_WITH_SOURCE,
    data: {
      content: 'You require administrator permissions to use this command.',
      flags: InteractionResponseFlags.EPHEMERAL,
    },
  });
}

async function fetchUserInfo(userId, env) {
  const apiEndpoint = `https://discord.com/api/v10/users/${userId}`;
  const response = await fetch(apiEndpoint, {
    method: 'GET',
    headers: {
      'Authorization': `Bot ${env.DISCORD_TOKEN}`,
      'Content-Type': 'application/json'
    }
  });
  if (response.ok) {
    const user = await response.json();
    console.log(`Successfully fetched info for user ${userId}: ${JSON.stringify(user)}`);
    return user;
  } else {
    console.error(`Failed to fetch info for user ${userId}`);
    return null;
  }
}

/**
 * page to verify if worker is online
 */
router.get('/', (request, env) => {
  return new Response(`I'm hereeeeeeee ${env.DISCORD_APPLICATION_ID}`);
});

router.post('/', async (request, env) => {
  const { isValid, interaction } = await server.verifyDiscordRequest(
    request,
    env,
  );
  if (!isValid || !interaction) {
    return new Response('Bad request signature', { status: 401 });
  }

  if (interaction.type === InteractionType.PING) {
    // required to configure the webhook in the developer portal
    return new JsonResponse({
      type: InteractionResponseType.PONG,
    });
  }

  if (interaction.type === InteractionType.APPLICATION_COMMAND) {
    const commandName = interaction.data.name.toLowerCase();
    const subCommand = interaction.data.options && interaction.data.options[0] && interaction.data.options[0].name.toLowerCase();
    const options = interaction.data.options;
    const channel = interaction.channel;
    const household_json = await env.HOUSEHOLDS_KV.get(channel.id);
    const household_keys = (await env.HOUSEHOLDS_KV.list()).keys;
    let household = null;
    if (household_json) {
      household = Object.assign(new Household, JSON.parse(household_json));
      console.log(JSON.stringify(household));
    } else {
      console.log("No household found");
    }
    console.log(`Command: ${commandName} ${subCommand} --- Channel: ${channel.name}, ${channel.id} --- Households: ${household_keys.length}`);

    console.log('Options:', options);
    let msg = '';

    
    switch (commandName) {
        
      case HOUSE_GROUP_COMMAND.name.toLowerCase():
        switch (subCommand) {
            
          case 'create':
            try {
              if (!hasAdminPermissions(interaction.member)) {
                return getNoAdminWarning();
              }
              const name = options[0].options[0].value;
              if (!household) {
                const newHousehold = new Household(name, channel);
                console.log(JSON.stringify(newHousehold));
                await env.HOUSEHOLDS_KV.put(channel.id, JSON.stringify(newHousehold));
                msg = `Household "${name}" created`;
              } else { msg = `Household "${household.name}" already uses this channel`; }
              console.log(msg);
              return new JsonResponse({
                type: InteractionResponseType.CHANNEL_MESSAGE_WITH_SOURCE,
                data: {
                  content: msg,
                  flags: InteractionResponseFlags.EPHEMERAL,
                },
              });
            } catch (error) {
              console.error(error);
            }
            break;
            
          case 'list':
            try {
              msg = `Households (${household_keys.length}):\n`;
              let hh = null;
              let hh_json = null;
              for (let household_key of household_keys) {
                hh_json = await env.HOUSEHOLDS_KV.get(household_key.name);
                console.log(`${household_key.name} ${hh_json}`);
                hh = Object.assign(new Household, JSON.parse(hh_json));
                msg = msg + `"${hh.name}" in "${hh.channel.name}" (${hh.users.length} users)\n`;
              }
              console.log(msg);
              return new JsonResponse({
                type: InteractionResponseType.CHANNEL_MESSAGE_WITH_SOURCE,
                data: {
                  content: msg.trim(),
                  flags: InteractionResponseFlags.EPHEMERAL,
                },
              });
            } catch (error) {
              console.error(error);
            }
            break;
            
          case 'delete':
            try {
              if (!hasAdminPermissions(interaction.member)) {
                return getNoAdminWarning();
              }
              if (household) {
                await env.HOUSEHOLDS_KV.delete(channel.id);
                msg = `Household "${household.name}" deleted`;
              } else {
                msg = 'No household found in this channel';
              }
              console.log(msg);
              return new JsonResponse({
                type: InteractionResponseType.CHANNEL_MESSAGE_WITH_SOURCE,
                data: {
                  content: msg,
                  flags: InteractionResponseFlags.EPHEMERAL,
                },
              });
            } catch (error) {
              console.error(error);
            }
            break;
            
          default:
            return new JsonResponse({ error: `Unknown ${commandName} subcommand` }, { status: 400 });
        }
        break;

      case USER_GROUP_COMMAND.name.toLowerCase():
        switch (subCommand) {

          case 'add':
            try {
              if (!hasAdminPermissions(interaction.member)) {
                return getNoAdminWarning();
              }
              const userId = options[0].options[0].value;
              const user = await fetchUserInfo(userId, env);
              if (!user) {
                return new JsonResponse({
                  type: InteractionResponseType.CHANNEL_MESSAGE_WITH_SOURCE,
                  data: {
                    content: `Failed to retrieve user ${userId}`,
                    flags: InteractionResponseFlags.EPHEMERAL,
                  },
                });
              }
              if (household) {
                if (!household.getUserById(userId)) {
                  household.addUser(user);
                  await env.HOUSEHOLDS_KV.put(channel.id, JSON.stringify(household));
                  msg = `User "${user.global_name}" added to household "${household.name}"`;
                } else {
                  msg = `User "${user.global_name}" already in household "${household.name}"`;
                }
              } else {
                msg = 'No household found in this channel';
              }
              console.log(msg);
              return new JsonResponse({
                type: InteractionResponseType.CHANNEL_MESSAGE_WITH_SOURCE,
                data: {
                  content: msg,
                  flags: InteractionResponseFlags.EPHEMERAL,
                },
              });
            } catch (error) {
              console.error(error);
            }
            break;

          case 'list':
            try {
              if (household) {
                msg = `Users in "${household.name}" (${household.users.length}):\n`;
                for (let user of household.users) {
                  msg = msg + `<@${user.id}> (${user.global_name})\n`;
                }
              } else {
                msg = 'No household found in this channel';
              }
              console.log(msg);
              return new JsonResponse({
                type: InteractionResponseType.CHANNEL_MESSAGE_WITH_SOURCE,
                data: {
                  content: msg.trim(),
                  flags: InteractionResponseFlags.EPHEMERAL,
                },
              });
            } catch (error) {
              console.error(error);
            }
            break;

          case 'remove':
            try {
              if (!hasAdminPermissions(interaction.member)) {
                return getNoAdminWarning();
              }
              const userId = options[0].options[0].value;
              if (household) {
                const user = household.getUserById(userId);
                if (user) {
                  household.removeUser(user);
                  await env.HOUSEHOLDS_KV.put(channel.id, JSON.stringify(household));
                  msg = `User "${user.global_name}" removed from household "${household.name}"`;
                } else {
                  msg = `User id "${userId}" not in household "${household.name}"`;
                }
              } else {
                msg = 'No household found in this channel';
              }
              console.log(msg);
              return new JsonResponse({
                type: InteractionResponseType.CHANNEL_MESSAGE_WITH_SOURCE,
                data: {
                  content: msg,
                  flags: InteractionResponseFlags.EPHEMERAL,
                },
              });
            } catch (error) {
              console.error(error);
            }
            break;

          default:
            return new JsonResponse({ error: `Unknown ${commandName} subcommand` }, { status: 400 });
        }
        break;

      default:
        return new JsonResponse({ error: 'Unknown command' }, { status: 400 });
    }
  }

  console.error('Unknown Type');
  return new JsonResponse({ error: 'Unknown interaction type' }, { status: 400 });
});
router.all('*', () => new Response('Not found', { status: 404 }));

async function verifyDiscordRequest(request, env) {
  const signature = request.headers.get('x-signature-ed25519');
  const timestamp = request.headers.get('x-signature-timestamp');
  const body = await request.text();
  const isValidRequest =
    signature &&
    timestamp &&
    (await verifyKey(body, signature, timestamp, env.DISCORD_PUBLIC_KEY));
  if (!isValidRequest) {
    return { isValid: false };
  }

  return { interaction: JSON.parse(body), isValid: true };
}

const server = {
  verifyDiscordRequest,
  fetch: router.fetch,
};

export default server;
