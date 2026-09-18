import {
    initializeApp
} from "https://www.gstatic.com/firebasejs/12.3.0/firebase-app.js";

import {
    getFirestore
} from "https://www.gstatic.com/firebasejs/12.3.0/firebase-firestore.js";


const firebaseConfig = {
    apiKey: "AIzaSyDCdnu1Pb_Vn1tZQfXlKyFgr1J-_yOkxAs",
    authDomain: "sentinel-2e53f.firebaseapp.com",
    projectId: "sentinel-2e53f",
    storageBucket: "sentinel-2e53f.firebasestorage.app",
    messagingSenderId: "419872261071",
    appId: "1:419872261071:web:9ef26310cc7d85945c88ba"
};


const app = initializeApp(firebaseConfig);

export const db = getFirestore(app);
