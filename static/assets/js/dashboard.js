// Import the functions you need from the SDKs you need
import { initializeApp } from 'https://www.gstatic.com/firebasejs/9.8.1/firebase-app.js';
import { getAuth, signOut, onAuthStateChanged } from 'https://www.gstatic.com/firebasejs/9.8.1/firebase-auth.js';
import { getFirestore, addDoc, collection } from 'https://www.gstatic.com/firebasejs/9.8.1/firebase-firestore.js';
// https://firebase.google.com/docs/web/setup#available-libraries

// Your web app's Firebase configuration
// For Firebase JS SDK v7.20.0 and later, measurementId is optional
const firebaseConfig = {
	apiKey: 'AIzaSyBRrZ3YTNm27johL82KS0tGrmP354nxAe8',
	authDomain: 'gbolahan-dfd2d.firebaseapp.com',
	projectId: 'gbolahan-dfd2d',
	storageBucket: 'gbolahan-dfd2d.appspot.com',
	messagingSenderId: '136569233948',
	appId: '1:136569233948:web:3f3acafa4a4a14114a35d9',
	measurementId: 'G-KHXG2FZFMV'
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);
const auth = getAuth();

// HANDLE LOGOUT
document.querySelector('#logout').addEventListener('click', e => {
	signOut(auth).then(() => {
		window.location.href = '/auth.html';
	});
});

// Make sure user is signed in
onAuthStateChanged(auth, user => {
	if (!user) window.location.href = '/auth.html';
	else {
		document.querySelector('#userName').innerHTML = user.email;
		document.querySelector('#userName_dropdown').innerHTML = user.email;
	}
});
