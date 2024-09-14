import { AutoRouter } from 'itty-router';
import {
  InteractionResponseType,
  InteractionType,
  InteractionResponseFlags,
  verifyKey,
} from 'discord-interactions';
import {
  HOUSE_GROUP_COMMAND,
} from './commands.js';

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
    switch (interaction.data.name.toLowerCase()) {
      case HOUSE_GROUP_COMMAND.toLowerCase(): {
        return new JsonResponse({
          type: interactionResponseType.CHANNEL_MESSAGE_WITH_SOURCE,
          data: {
            content: 'Hello',
            flags: InteractionResponseFlags.EPHEMERAL,
          },
        });
      }
      case default:
        return new JsonResponse({ error: 'Unknown interaction command' }, { status: 400 });
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
  const isValidrequest =
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
