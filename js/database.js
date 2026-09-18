import {
    collection,
    addDoc,
    getDocs,
    doc,
    updateDoc,
    deleteDoc
} from "https://www.gstatic.com/firebasejs/12.3.0/firebase-firestore.js";

import { db } from "./firebase.js";

const transactionsRef = collection(db, "transactions");


// SAVE TRANSACTION
export async function saveTransaction(transaction) {
    try {
        const docRef = await addDoc(transactionsRef, {
            ...transaction,
            createdAt: new Date()
        });

        console.log("Transaction saved:", docRef.id);

        return docRef.id;

    } catch (error) {
        console.error("Error saving transaction:", error);

        // Send the error back to risk-analysis.html
        throw error;
    }
}


// GET ALL TRANSACTIONS
export async function getTransactions() {
    try {
        const snapshot = await getDocs(transactionsRef);

        return snapshot.docs.map(doc => ({
            id: doc.id,
            ...doc.data()
        }));

    } catch (error) {
        console.error("Error loading transactions:", error);

        return [];
    }
}


// UPDATE TRANSACTION
export async function updateTransaction(id, data) {
    try {
        await updateDoc(
            doc(db, "transactions", id),
            data
        );

        console.log("Transaction updated");

    } catch (error) {
        console.error("Error updating transaction:", error);

        throw error;
    }
}


// DELETE TRANSACTION
export async function deleteTransaction(id) {
    try {
        await deleteDoc(
            doc(db, "transactions", id)
        );

        console.log("Transaction deleted");

    } catch (error) {
        console.error("Error deleting transaction:", error);

        throw error;
    }
}
