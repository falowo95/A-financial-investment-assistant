// Import the functions you need from the SDKs you need

import { initializeApp } from 'https://www.gstatic.com/firebasejs/9.8.1/firebase-app.js';
import {
	getAuth,
	createUserWithEmailAndPassword,
	signInWithEmailAndPassword
} from 'https://www.gstatic.com/firebasejs/9.8.1/firebase-auth.js';
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
const db = getFirestore(app);
//through db variable you can communicate with firestore
/**
 * SET VIEW (LOGIN OR SIGN UP)
 */
function setView(view) {
	const signUpButton = document.querySelector('#signUpButton');
	const loginButton = document.querySelector('#loginButton');
	const signUpForm = document.querySelector('#signUpForm');
	const loginForm = document.querySelector('#loginForm');

	signUpButton.className = view === 'signUp' ? 'active' : '';
	loginButton.className = view === 'login' ? 'active' : '';
	signUpForm.className = view === 'signUp' ? 'show' : 'hide';
	loginForm.className = view === 'login' ? 'show' : 'hide';
}

document.querySelector('#signUpButton').addEventListener('click', () => {
	setView('signUp');
	document.querySelector('#formError').innerHTML = ``;
});

document.querySelector('#loginButton').addEventListener('click', () => {
	setView('login');
	document.querySelector('#formError').innerHTML = ``;
});

/**
 * ON SIGN UP
 */
const signUpForm = document.querySelector('#signUpForm');
signUpForm.addEventListener('submit', e => {
	e.preventDefault();
	const name = signUpForm.name.value;
	const email = signUpForm.email.value;
	const password = signUpForm.password.value;

	// Sign Up
	createUserWithEmailAndPassword(auth, email, password)
		.then(cred => {
			// Create user
			addDoc(collection(db, 'users'), { name, email, uid: cred.user.uid })
				.then(e => {
					window.location.href = '/dashboard.html';
				})
				.catch(e => {
					document.querySelector('#formError').innerHTML = `<p>${e.message}</p>`;
				});
		})
		.catch(e => {
			document.querySelector('#formError').innerHTML = `<p>${e.message}</p>`;
		});
});

/**
 * ON LOGIN
 */
const loginForm = document.querySelector('#loginForm');
loginForm.addEventListener('submit', e => {
	e.preventDefault();
	const email = loginForm.email.value;
	const password = loginForm.password.value;

	// Handle login
	signInWithEmailAndPassword(auth, email, password)
		.then(cred => {
			window.location.href = '/dashboard.html';
		})
		.catch(e => {
			document.querySelector('#formError').innerHTML = `<p>${e.message}</p>`;
		});
});
