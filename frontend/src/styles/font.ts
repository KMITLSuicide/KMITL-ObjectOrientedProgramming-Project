import localFont from "next/font/local";

export const inter = localFont({
  src: [
    { path: "./inter-variable/InterVariable.woff2", style: "normal" },
    {
      path: "./inter-variable/InterVariable-Italic.woff2",
      style: "italic",
    },
  ],
});
