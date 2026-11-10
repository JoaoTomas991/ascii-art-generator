# 0006. Drawings are shared to chat apps as an image, not as a text block

Date: 2026-11-09
Status: Accepted

## Context

The browser version had a **Copy for WhatsApp, Telegram…** button. It copied
the drawing as plain text wrapped in triple backticks, which WhatsApp,
Telegram, Discord and Slack show in a monospace font, so the columns line up.

Trying it with a red heart showed two problems:

- The color was lost. A monospace block in a chat app is plain text and has
  no way to color it, and sending the ANSI codes would only show them as
  garbage.
- The same message looked right in WhatsApp Web and broken in WhatsApp on a
  phone. The heart is 44 columns wide at `size 4` and 64 at the default
  size. The desktop bubble was wide enough for it; the phone bubble was not,
  so every long line wrapped and the shape fell apart.

The second problem cannot be fixed from our side, because a monospace block
is not the same thing everywhere. How many columns fit on a line depends on
the app, on whether it is the desktop or the phone version, on the screen
width and on the reader's font size. The sender cannot know what the
receiver's screen will fit, and the page's warning for drawings wider than
36 columns was a guess that was too generous for a phone.

## Decision

The browser version shares drawings to chat apps as a picture. A **Copy as
image** button paints the drawing on a canvas, with the result panel's font,
colors and background, and copies it to the clipboard as a PNG. A browser
that cannot copy images downloads the file instead.

The **Copy for WhatsApp, Telegram…** button and its triple-backtick wrapping
were removed. **Copy text** stays, for places where plain text is what is
wanted.

## Alternatives considered

- Keeping both buttons would leave a button that is named after the chat
  apps and gives a broken result in one of them, next to one that works.
- Lowering the width warning, or refusing wide drawings, would still depend
  on a column limit nobody can know, and would not bring the color back.
- Shrinking the drawing to fit a phone would change what the user drew, and
  shapes such as the default heart have no version that narrow.
- Copying rich text (HTML with colors) is ignored by the chat apps, which
  paste plain text.

## Consequences

- A shared drawing looks the same on every screen and keeps its colors,
  including the true-color output of `convert image`.
- The receiver gets a picture, so the drawing can no longer be selected or
  copied as text from the chat. **Copy text** covers that case, without the
  monospace wrapping.
- Copying an image needs a secure context (https or localhost) and a browser
  with image clipboard support. Everywhere else the button falls back to a
  download, which takes one more step to send.
- The picture is capped at 4096 pixels on its longest side, because larger
  canvases fail in some browsers. Very large drawings are scaled down.
- The terminal has no equivalent yet. Saving a drawing as a PNG from the
  command line is on the roadmap.
