import type { Metadata } from "next";
import { Outfit } from "next/font/google";
import "./globals.css";
import Sidebar from "@/components/Sidebar";

const outfit = Outfit({
  variable: "--font-outfit",
  subsets: ["latin"],
});

export const metadata: Metadata = {
  title: "EPC Intelligence Platform",
  description: "Advanced Data Centre EPC Project Intelligence Platform",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html
      lang="en"
      className={`${outfit.variable} h-full antialiased dark`}
    >
      <body className="min-h-full flex">
        <Sidebar />
        <main className="ml-64 flex-1 p-8 overflow-y-auto">
          {children}
        </main>
      </body>
    </html>
  );
}
