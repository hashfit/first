# HASHFIT apply site

Two pages, both in the HASHFIT branding:

| Page | Folder | What it's for |
|---|---|---|
| Pre-call | `precall/` | Where people land straight after they book. Plays the pre-call video and tells them to send you the word from the end. |
| VSL | `vsl/` | The page you send people manually. Plays the VSL, with your Discovery Call booking box under it. Booking from here sends them straight to the pre-call page. |

`assets/` holds the logo, the styles and the video player code that both pages share. Keep the three folders together when you upload.

## 1. Get the videos online

The pages play a video from a link, so each video needs to be uploaded somewhere first. Pick one:

- **YouTube, set to Unlisted.** Free and easiest. Nobody finds it unless they have the page.
- **Wistia.** Has a free plan, and the pre-call page tags each view with the person's email (from Calendly). You can then see how much of the video each person watched before the call.
- Vimeo, Loom or a Google Drive link (set to "Anyone with the link") also work.

## 2. Paste the links in

Open `precall/index.html` and `vsl/index.html`. Near the top of each there's a block that says `EDIT THESE`. Paste the link between the quotes on the `videoUrl` line:

```js
videoUrl: "https://youtu.be/your-video-id",
```

If you filmed it upright on your phone, change `vertical: false` to `vertical: true`.

On the pre-call page, `replyTo` is where people send you the word from the end of the video. Change it to wherever you want the reply, for example `"in my Instagram DMs"`.

## 3. Put it online

Upload the whole `apply-site` folder to your host (Netlify, Vercel, GitHub Pages, or your site's file manager). The pages end up at:

- `yourdomain/precall/`
- `yourdomain/vsl/`

On Netlify you can drag the folder straight onto app.netlify.com/drop and connect your domain afterwards.

## 4. Send Calendly bookings to the pre-call page

Bookings made on the VSL page already redirect to the pre-call page.

To redirect people who book from your plain Calendly link too (paid Calendly plan needed):

1. Calendly, then Discovery Call, then Edit.
2. Booking page options, then Confirmation page.
3. Choose **Redirect to an external site** and paste `https://yourdomain/precall/`.
4. Tick **Pass event details to your redirected page**. The page then greets them by first name and shows their call time.

Without the paid plan, send people to the VSL page instead of the raw Calendly link. The redirect works there on the free plan.
