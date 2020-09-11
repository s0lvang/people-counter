import React, { useState } from "react";
import logo from "./logo.svg";
import "./App.css";
import {
  FirebaseDatabaseProvider,
  FirebaseDatabaseNode,
} from "@react-firebase/database";
import firebase from "firebase";
const firebaseConfig = {
  apiKey: "AIzaSyAnphCSHQTmiNlHOLWZcq5QvtyizMaRfXY",
  authDomain: "people-counter-4f7dc.firebaseapp.com",
  databaseURL: "https://people-counter-4f7dc.firebaseio.com",
  projectId: "people-counter-4f7dc",
  storageBucket: "people-counter-4f7dc.appspot.com",
  messagingSenderId: "688418173450",
  appId: "1:688418173450:web:ee2f7dd4b61602b5bba5f3",
  measurementId: "G-XGGGFTYBF6",
};
firebase.initializeApp(firebaseConfig);

function App() {
  const [numberOfPersons, setnumberOfPersons] = useState(0);
  return (
    <FirebaseDatabaseProvider firebase={firebase}>
      <div className="App">
        <FirebaseDatabaseNode
          path="/"
          // orderByKey
          orderByValue={"created_on"}
        >
          {(t) => t.value}
        </FirebaseDatabaseNode>
      </div>
    </FirebaseDatabaseProvider>
  );
}

export default App;
