import Footer from "@/components/shared/footer/footer";
import MobileMenu from "@/components/shared/footer/mobile-menu";
import Header from "@/components/shared/header/header";
import type { Metadata } from "next";
import { Geist, Geist_Mono } from "next/font/google";
import "./globals.css";
import QueryProvider from "@/hooks/query-provider";
import { Toaster } from "@/components/ui/sonner";

const geistSans = Geist({
  variable: "--font-geist-sans",
  subsets: ["latin"],
});

const geistMono = Geist_Mono({
  variable: "--font-geist-mono",
  subsets: ["latin"],
});

export const metadata: Metadata = {
  title: "ShopSphere",
  description: "Multi Vendor Saas Ecommerce",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body
        className={`${geistSans.variable} ${geistMono.variable} antialiased`}
      >
        <div className="min-h-screen bg-gradient-to-t from-[#c1dfc4] to-[#deecdd] pt-5 md:pt-7 lg:pt-10 px-5 md:px-10 lg:px-16">
          <Header />
          <main>
            <QueryProvider>{children}</QueryProvider>
          </main>
          <Footer />
          <MobileMenu />
        </div>
        <Toaster position="top-right" />
      </body>
    </html>
  );
}
