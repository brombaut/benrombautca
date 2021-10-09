"use strict";
var __awaiter = (this && this.__awaiter) || function (thisArg, _arguments, P, generator) {
    function adopt(value) { return value instanceof P ? value : new P(function (resolve) { resolve(value); }); }
    return new (P || (P = Promise))(function (resolve, reject) {
        function fulfilled(value) { try { step(generator.next(value)); } catch (e) { reject(e); } }
        function rejected(value) { try { step(generator["throw"](value)); } catch (e) { reject(e); } }
        function step(result) { result.done ? resolve(result.value) : adopt(result.value).then(fulfilled, rejected); }
        step((generator = generator.apply(thisArg, _arguments || [])).next());
    });
};
var __generator = (this && this.__generator) || function (thisArg, body) {
    var _ = { label: 0, sent: function() { if (t[0] & 1) throw t[1]; return t[1]; }, trys: [], ops: [] }, f, y, t, g;
    return g = { next: verb(0), "throw": verb(1), "return": verb(2) }, typeof Symbol === "function" && (g[Symbol.iterator] = function() { return this; }), g;
    function verb(n) { return function (v) { return step([n, v]); }; }
    function step(op) {
        if (f) throw new TypeError("Generator is already executing.");
        while (_) try {
            if (f = 1, y && (t = op[0] & 2 ? y["return"] : op[0] ? y["throw"] || ((t = y["return"]) && t.call(y), 0) : y.next) && !(t = t.call(y, op[1])).done) return t;
            if (y = 0, t) op = [op[0] & 2, t.value];
            switch (op[0]) {
                case 0: case 1: t = op; break;
                case 4: _.label++; return { value: op[1], done: false };
                case 5: _.label++; y = op[1]; op = [0]; continue;
                case 7: op = _.ops.pop(); _.trys.pop(); continue;
                default:
                    if (!(t = _.trys, t = t.length > 0 && t[t.length - 1]) && (op[0] === 6 || op[0] === 2)) { _ = 0; continue; }
                    if (op[0] === 3 && (!t || (op[1] > t[0] && op[1] < t[3]))) { _.label = op[1]; break; }
                    if (op[0] === 6 && _.label < t[1]) { _.label = t[1]; t = op; break; }
                    if (t && _.label < t[2]) { _.label = t[2]; _.ops.push(op); break; }
                    if (t[2]) _.ops.pop();
                    _.trys.pop(); continue;
            }
            op = body.call(thisArg, _);
        } catch (e) { op = [6, e]; y = 0; } finally { f = t = 0; }
        if (op[0] & 5) throw op[1]; return { value: op[0] ? op[1] : void 0, done: true };
    }
};
exports.__esModule = true;
var fs = require("fs");
var types_1 = require("@brombaut/types");
// import { firebaseConfig } from './firebase.config';
var firebase_firestore_facade_1 = require("firebase-firestore-facade");
// import dotenv = require('dotenv');
var dotenv = require("dotenv");
dotenv.config();
var firebaseConfig = {
    apiKey: process.env.VUE_APP_API_KEY || '',
    authDomain: process.env.VUE_APP_AUTH_DOMAIN || '',
    projectId: process.env.VUE_APP_PROJECT_ID || '',
    storageBucket: process.env.VUE_APP_STORAGE_BUCKET || '',
    messagingSenderId: process.env.VUE_APP_MESSAGING_SENDER_ID || '',
    appId: process.env.VUE_APP_APP_ID || '',
    measurementId: process.env.VUE_APP_MEASUREMENT_ID || '',
    auth: {
        email: process.env.VUE_APP_TEST_USER_EMAIL || '',
        password: process.env.VUE_APP_TEST_USER_PASSWORD || ''
    }
};
function main() {
    return __awaiter(this, void 0, void 0, function () {
        var f3, booksFromGoodreads, f3Books, existingF3Books, newF3Books;
        return __generator(this, function (_a) {
            switch (_a.label) {
                case 0:
                    console.log("Starting Sync");
                    console.log("Init F3Bookshelf");
                    return [4 /*yield*/, new types_1.F3Bookshelf(firebaseConfig).init()];
                case 1:
                    f3 = _a.sent();
                    console.log("Reading translated goodreads book file");
                    booksFromGoodreads = readTranslatedBooksFile();
                    console.log("Fetching existing F3 books");
                    return [4 /*yield*/, fetchF3Books(f3)];
                case 2:
                    f3Books = _a.sent();
                    console.log("Syncing existing F3 books");
                    existingF3Books = syncExistingF3Books(f3Books, booksFromGoodreads);
                    console.log("Updating F3 with synced books");
                    return [4 /*yield*/, updateF3WithSyncedBooks(f3, existingF3Books)];
                case 3:
                    _a.sent();
                    console.log("Creating new F3 books");
                    newF3Books = createNewF3Books(f3Books, booksFromGoodreads);
                    console.log("Updating F3 with added books");
                    return [4 /*yield*/, addNewBooksToF3(f3, newF3Books)];
                case 4:
                    _a.sent();
                    console.log("Closing F3 Connection");
                    return [4 /*yield*/, f3.closeConnection()];
                case 5:
                    _a.sent();
                    console.log("Done");
                    return [2 /*return*/];
            }
        });
    });
}
function readTranslatedBooksFile() {
    // TODO: Make the working directory a command line argument or env var
    var data = fs.readFileSync('./src/bookshelf/syncer/translated_books_from_gr.json', 'utf8');
    return JSON.parse(data);
}
function fetchF3Books(f3) {
    return __awaiter(this, void 0, void 0, function () {
        var books;
        return __generator(this, function (_a) {
            switch (_a.label) {
                case 0: return [4 /*yield*/, f3.get()];
                case 1:
                    books = _a.sent();
                    return [2 /*return*/, books];
            }
        });
    });
}
function syncExistingF3Books(f3Books, grBooks) {
    var result = [];
    f3Books.forEach(function (b) {
        var grBook = grBooks.find(function (grb) { return grb.goodreads_review_id === b.goodreads_review_id; });
        if (!grBook)
            return;
        var needsSyncing = false;
        if (grBook.shelf == types_1.Shelf.CURRENTLYREADING && b.shelf == types_1.Shelf.TOREAD) {
            b.startReading();
            needsSyncing = true;
        }
        if (grBook.shelf == types_1.Shelf.READ && b.shelf == types_1.Shelf.CURRENTLYREADING) {
            b.finishedReading();
            needsSyncing = true;
        }
        if (b.onPage !== null && grBook.on_page !== null) {
            var changedAndGROnPageIsHigher = b.onPage !== grBook.on_page && grBook.on_page > b.onPage;
            if (changedAndGROnPageIsHigher) {
                b.onPage = grBook.on_page;
                needsSyncing = true;
            }
        }
        if (b.rating !== parseInt(grBook.rating)) {
            b.rating = parseInt(grBook.rating);
            needsSyncing = true;
        }
        var grIsbnIsDifferentThanF3 = grBook.isbn13 && b.isbn13 !== grBook.isbn13;
        if (grIsbnIsDifferentThanF3) {
            console.warn("WARNING - ReviewID=" + b.goodreads_review_id + " title=" + b.title + " :: ISBN13 do not match :: f3.isbn13=" + b.isbn13 + " gr.isbn13=" + grBook.isbn13);
        }
        if (needsSyncing) {
            result.push(b);
        }
    });
    return result;
}
function updateF3WithSyncedBooks(f3, syncedF3Books) {
    return __awaiter(this, void 0, void 0, function () {
        var _i, syncedF3Books_1, b;
        return __generator(this, function (_a) {
            switch (_a.label) {
                case 0:
                    _i = 0, syncedF3Books_1 = syncedF3Books;
                    _a.label = 1;
                case 1:
                    if (!(_i < syncedF3Books_1.length)) return [3 /*break*/, 4];
                    b = syncedF3Books_1[_i];
                    return [4 /*yield*/, f3.put(b)];
                case 2:
                    _a.sent();
                    _a.label = 3;
                case 3:
                    _i++;
                    return [3 /*break*/, 1];
                case 4: return [2 /*return*/];
            }
        });
    });
}
function createNewF3Books(f3Books, grBooks) {
    var newGRBooks = [];
    grBooks.forEach(function (grb) {
        var i = f3Books.findIndex(function (b) { return b.goodreads_review_id === grb.goodreads_review_id; });
        if (i < 0) {
            newGRBooks.push(grb);
        }
    });
    var newFirestoreBooks = newGRBooks.map(function (grb) {
        var sDate = null;
        if (grb.dateStarted) {
            sDate = new firebase_firestore_facade_1.FirestoreDateTranslator().fromDate(new Date(grb.dateStarted)).toFirestoreDate();
        }
        var fDate = null;
        if (grb.dateFinished) {
            fDate = new firebase_firestore_facade_1.FirestoreDateTranslator().fromDate(new Date(grb.dateFinished)).toFirestoreDate();
        }
        return {
            id: '',
            goodreads_review_id: grb.goodreads_review_id,
            isbn13: grb.isbn13,
            title: grb.title,
            shortTitle: grb.short_title,
            authors: [grb.authors],
            numPages: grb.num_pages || 0,
            link: grb.link,
            shelf: grb.shelf,
            onPage: grb.on_page,
            dateStarted: sDate,
            dateFinished: fDate,
            rating: parseInt(grb.rating)
        };
    });
    return newFirestoreBooks;
}
function addNewBooksToF3(f3, newBooks) {
    return __awaiter(this, void 0, void 0, function () {
        var _i, newBooks_1, fb;
        return __generator(this, function (_a) {
            switch (_a.label) {
                case 0:
                    _i = 0, newBooks_1 = newBooks;
                    _a.label = 1;
                case 1:
                    if (!(_i < newBooks_1.length)) return [3 /*break*/, 4];
                    fb = newBooks_1[_i];
                    return [4 /*yield*/, f3.post(fb)];
                case 2:
                    _a.sent();
                    _a.label = 3;
                case 3:
                    _i++;
                    return [3 /*break*/, 1];
                case 4: return [2 /*return*/];
            }
        });
    });
}
main();
