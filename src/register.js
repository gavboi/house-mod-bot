import { HOUSE_GROUP_COMMAND } from './commands.js';

/**
 * run from command line on command definition changes
 */

 const token = process.env.DISCORD_TOKEN;
 const applicationId = process.env.DISCORD_APPLICATION_ID;

 if (!token) {
   throw new Error('The DISCORD_TOKEN environment variable is required.');
 }
 if (!applicationId) {
   throw new Error('The DISCORD_APPLICATION_ID environment variable is required.');
 }

 async function registerCommands(url) {
   const response = await fetch(url, {
     headers: {
       'Content-Type': 'application/json',
       Authorization: `Bot ${token}`,
     },
     method: 'PUT',
     body: JSON.stringify([HOUSE_GROUP_COMMAND]),
   });

   if (response.ok) {
     console.log('Registered all commands');
   } else {
     console.error('Error registering commands');
     const text = await response.text();
     console.error(text);
   }
   return response;
 }

 await registerGlobalCommands();
