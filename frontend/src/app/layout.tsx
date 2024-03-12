import "~/src/styles/globals.css";
import { inter } from "~/src/styles/font";
import { ThemeProvider } from "~/src/components/theme-provider";
import NavBar from "~/src/components/navbar/navbar";
import { Toaster } from "~/src/components/ui/toaster";

export const metadata = {
  title: {
    template: '%s | "Udemy"',
    default: '"Udemy"',
  },
  description: "THE very real udemy",
  icons: [{ rel: "icon", url: "/favicon.jpg" }],
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <head></head>
      <body className={`font-sans ${inter.className}`}>
        <ThemeProvider
          attribute="class"
          defaultTheme="system"
          enableSystem
          disableTransitionOnChange
        >
          <NavBar className="px-4" />
          <main className="h-[calc(100vh-3rem)] p-4">{children}</main>
          <Toaster />
        </ThemeProvider>
      </body>
    </html>
  );
}
