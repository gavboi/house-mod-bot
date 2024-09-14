export const HOUSE_GROUP_COMMAND = {
  name: 'house',
  description: 'Manage households',
  options: [
    {
      type: 'SUB_COMMAND',
      name: 'create',
      description: 'Create household in current channel',
      options: [
        {
          type: 'STRING',
          name: 'name',
          description: 'Name of household',
          required: true,
        },
      ],
    },
    {
      type: 'SUB_COMMAND',
      name: 'list',
      description: 'List all households',
    },
    {
      type: 'SUB_COMMAND',
      name: 'delete',
      description: 'Delete household in current channel',
    },
  ],
};