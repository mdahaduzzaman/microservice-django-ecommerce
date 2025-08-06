export { auth as middleware } from "@/auth"
// import { NextRequest, NextResponse } from "next/server";
// import { auth } from "@/auth";

// export default auth((request: NextRequest) => {
//   const requestHeaders = new Headers(request.headers);
//   requestHeaders.set("x-current-url", request.nextUrl.href);
//   requestHeaders.set("x-current-path", request.nextUrl.pathname);

//   const response = NextResponse.next({
//     request: {
//       headers: requestHeaders,
//     },
//   });

//   return response;
// });

// export const config = {
//   matcher: [
//     /**
//      * Match all routes except:
//      * - /api/auth/*
//      * - /_next/*
//      * - /static/*
//      * - /favicon.ico
//      * - /login
//      */
//     "/((?!api/auth|_next/static|_next/image|favicon.ico|login|register).*)",
//   ],
// };
