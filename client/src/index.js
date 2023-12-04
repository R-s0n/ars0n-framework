import React, { createContext, useContext } from 'react';
import ReactDOM from 'react-dom/client';
import './index.css';
import App from './App';
import reportWebVitals from './reportWebVitals';
import 'bootstrap/dist/css/bootstrap.css';
import './custom.scss';

const root = ReactDOM.createRoot(document.getElementById('root'));

const ApiContext = createContext({
  flaskHost: process.env.REACT_APP_FLASK_API_HOST || 'http://localhost:5000',
  nodeHost: process.env.REACT_APP_NODE_API_HOST || 'http://localhost:8000',
});

export const useApi = () => {
  const api = useContext(ApiContext);
  return api;
}

root.render(
  <React.StrictMode>
    <ApiContext.Provider>
      <App />
    </ApiContext.Provider>
  </React.StrictMode>
);

// If you want to start measuring performance in your app, pass a function
// to log results (for example: reportWebVitals(console.log))
// or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals
reportWebVitals();
