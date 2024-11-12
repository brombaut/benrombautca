import * as fs from "fs";
import { Book, F3Bookshelf, FirestoreBook, Shelf } from "@brombaut/types";
import { FirestoreDateTranslator, FirebaseConfigurer } from "firebase-firestore-facade";
import * as dotenv from "dotenv";

dotenv.config({path: "../../../.env" });

const firebaseConfig: FirebaseConfigurer = {
    apiKey: process.env.VUE_APP_API_KEY || "",
    authDomain: process.env.VUE_APP_AUTH_DOMAIN || "",
    projectId: process.env.VUE_APP_PROJECT_ID || "",
    storageBucket: process.env.VUE_APP_STORAGE_BUCKET || "",
    messagingSenderId: process.env.VUE_APP_MESSAGING_SENDER_ID || "",
    appId: process.env.VUE_APP_APP_ID || "",
    measurementId: process.env.VUE_APP_MEASUREMENT_ID || "",
    auth: {
        email: process.env.VUE_APP_TEST_USER_EMAIL || "",
        password: process.env.VUE_APP_TEST_USER_PASSWORD || "",
    },
};

// const firebaseConfig: FirebaseConfigurer = {
//     apiKey: "AIzaSyCBA_Pg1g0BqAXq5LVZnPeQIqfTmsEfZBI",
//     authDomain: "benrombautca.firebaseapp.com",
//     projectId: "benrombautca",
//     storageBucket: "benrombautca.appspot.com",
//     messagingSenderId: "139659605759",
//     appId: "1:139659605759:web:311f00f9a364916ca83eca",
//     measurementId: "G-XFPZWMXJXK",
//     auth: {
//         email: "test@benrombaut.ca",
//         password: "vanilla"
//     },
// };


async function main() {
    console.log("Starting Sync");
    console.log("Init F3Bookshelf");
    const f3: F3Bookshelf = await new F3Bookshelf(firebaseConfig).init();

    console.log("Fetching existing F3 books");
    const f3Books: Book[] = await fetchF3Books(f3);

    // Write f3Books to a json file
    fs.writeFileSync('f3Books.json', JSON.stringify(f3Books, null, 2));

    console.log("Closing F3 Connection");
    await f3.closeConnection();

    console.log("Done");
}

async function fetchF3Books(f3: F3Bookshelf): Promise<Book[]> {
    const books: Book[] = await f3.get();
    return books;
}

main();
