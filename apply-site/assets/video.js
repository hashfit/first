/*
  Puts a video into a box on the page.
  Works with a YouTube, Vimeo, Loom, Wistia or Google Drive link,
  or a direct link to an .mp4 / .webm / .mov file.

  mountVideo(element, url, { vertical: false, email: "" })
  - vertical: true if you filmed it upright on your phone (9:16)
  - email: if the video is on Wistia, this tags the view with that person's
    email so Wistia shows you exactly how much of it they watched
*/
(function () {
  function youtubeId(u) {
    if (u.hostname === "youtu.be") return u.pathname.slice(1);
    if (u.searchParams.get("v")) return u.searchParams.get("v");
    var m = u.pathname.match(/\/(embed|shorts|live)\/([^/?]+)/);
    return m ? m[2] : null;
  }

  function embedSrc(raw, email) {
    var u;
    try { u = new URL(raw); } catch (e) { return null; }
    var host = u.hostname.replace(/^www\./, "");

    if (host === "youtube.com" || host === "m.youtube.com" || host === "youtu.be" || host === "youtube-nocookie.com") {
      var id = youtubeId(u);
      if (!id) return null;
      return { kind: "iframe", src: "https://www.youtube-nocookie.com/embed/" + id + "?rel=0&modestbranding=1&playsinline=1" };
    }

    if (host === "vimeo.com" || host === "player.vimeo.com") {
      var parts = u.pathname.split("/").filter(Boolean);
      if (parts[0] === "video") parts.shift();
      var vid = parts[0];
      var hash = parts[1] || u.searchParams.get("h");
      var src = "https://player.vimeo.com/video/" + vid + "?title=0&byline=0&portrait=0&dnt=1";
      if (hash) src += "&h=" + hash;
      return { kind: "iframe", src: src };
    }

    if (host === "loom.com") {
      var lm = u.pathname.match(/\/(share|embed)\/([^/?]+)/);
      if (!lm) return null;
      return { kind: "iframe", src: "https://www.loom.com/embed/" + lm[2] + "?hide_owner=true&hide_share=true&hide_title=true&hideEmbedTopBar=true" };
    }

    if (/wistia\.(com|net)$/.test(host)) {
      var wm = u.pathname.match(/\/(medias|iframe)\/([^/?]+)/);
      if (!wm) return null;
      var wsrc = "https://fast.wistia.net/embed/iframe/" + wm[2] + "?playerColor=E8312E";
      if (email) wsrc += "&wemail=" + encodeURIComponent(email);
      return { kind: "iframe", src: wsrc };
    }

    if (host === "drive.google.com") {
      var dm = u.pathname.match(/\/file\/d\/([^/]+)/);
      if (!dm) return null;
      return { kind: "iframe", src: "https://drive.google.com/file/d/" + dm[1] + "/preview" };
    }

    if (/\.(mp4|webm|mov|m4v)$/i.test(u.pathname)) {
      return { kind: "file", src: raw };
    }

    return { kind: "iframe", src: raw };
  }

  window.mountVideo = function (box, url, opts) {
    opts = opts || {};
    if (opts.vertical) box.classList.add("vertical");

    var found = url && url.trim() ? embedSrc(url.trim(), opts.email) : null;
    if (!found) return; // leaves the "video coming soon" box in place

    box.innerHTML = "";
    if (found.kind === "file") {
      var v = document.createElement("video");
      v.src = found.src;
      v.controls = true;
      v.playsInline = true;
      v.preload = "metadata";
      box.appendChild(v);
    } else {
      var f = document.createElement("iframe");
      f.src = found.src;
      f.title = opts.title || "Video";
      f.allow = "autoplay; fullscreen; picture-in-picture; encrypted-media";
      f.allowFullscreen = true;
      box.appendChild(f);
    }
  };
})();
