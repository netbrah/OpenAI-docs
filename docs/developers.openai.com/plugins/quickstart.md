# Quickstart

> For the complete documentation index, see [llms.txt](/llms.txt). Markdown versions of documentation pages are available by appending `.md` to the page URL.

Plugins extend and customize ChatGPT and Codex. They can add capabilities,
connect to external services, or both. A plugin can include skills that provide
instructions and resources, an MCP server that exposes tools, or both.

ChatGPT and Codex share one universal plugin directory. Public plugins are
published once and become discoverable from supported surfaces in both
products.

This tutorial creates a personal plugin by connecting an MCP server. By the
end, you will find the plugin in your personal Plugins directory and invoke its
tool from ChatGPT Work on the web. Custom UI is optional and is not part of
this quickstart.

This quickstart uses a public example MCP server at
  `https://tinymcp.dev/api/moldy-aloof-zettabyte/mcp`. It exposes a read-only
  `roll_dice` tool and does not require authentication.

## Connect your MCP server

First, add your deployed MCP server in ChatGPT developer mode:

1. Open [ChatGPT](https://chatgpt.com).
2. Open **Settings → Security and login** and turn on **Developer mode**.
3. Go to [ChatGPT Plugins](https://chatgpt.com/plugins), select the plus
   button, and enter
   `https://tinymcp.dev/api/moldy-aloof-zettabyte/mcp` as the MCP server URL.
4. Complete the connection details and create the plugin.

## Test the plugin

1. Go to [your personal plugins](https://chatgpt.com/plugins?view=personal).
   The plugin you created from the MCP server should appear there.
2. Open the plugin and select the plus button to install it.
3. Return to the [ChatGPT homepage](https://chatgpt.com).
4. At the top of the homepage, switch the tab from **Chat** to **Work**.
5. Start a new Work chat. In the prompt box, type `@` and select your plugin to
   invoke it directly.
6. Ask the plugin to roll one 20-sided die. Confirm that it calls `roll_dice`
   once with `sides` set to 20 and returns one value from 1 through 20.

Test several realistic inputs, including different die sizes, invalid values,
  and requests that should not call the tool. Refine the tool metadata when the
  wrong tool is selected or its arguments are inconsistent.

## Add more capabilities

Add more focused tools when the use-case inventory calls for them. To package
reusable instructions with the MCP server, continue with [Build
skills](https://developers.openai.com/plugins/build/skills) and [Package your
plugin](https://developers.openai.com/plugins/build/plugins). If a workflow benefits from visual
interaction, continue with [Add UI to your MCP
server](https://developers.openai.com/plugins/build/chatgpt-ui). UI remains optional.

## Publish the plugin

When the plugin is ready for other people, review the complete [plugin build
guide](https://developers.openai.com/plugins/build/plugins). To publish it publicly, use the [plugin
submission portal](https://developers.openai.com/plugins/deploy/submission).