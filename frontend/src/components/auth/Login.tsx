import { useState } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import { showMessage } from '../../utils/messages';
import type { MessageType } from '../../types';
import logo from "../../assets/logo.png";
import './Login.css';



function Login() {
  const [formData, setFormData] = useState({
    email: '',
    password: ''
  });
  const [message, setMessage] = useState({
    text: '',
    type: null as MessageType
  });
  const navigate = useNavigate();
  const location = useLocation();

  const handleLogin = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!formData.email || !formData.password) {
      showMessage('Please fill in all fields', 'error', setMessage);
      return;
    }

    try {
      const formDataInstance = new FormData();
      formDataInstance.append('username', formData.email);
      formDataInstance.append('password', formData.password);

      const response = await fetch('https://44.202.132.203:8000/login', {
        method: 'POST',
        body: formDataInstance,
      });
      
      const data = await response.json();
      
      if (response.ok) {
        localStorage.setItem('token', data.access_token);
        navigate('/home');
      } else {
        showMessage(data.detail || 'Invalid credentials', 'error', setMessage);
      }
    } catch (error) {
      console.error('Login error:', error);
      showMessage('Login failed. Please try again.', 'error', setMessage);
    }
  };

  const handleRegister = () => {
    navigate('/register');
  }

  const loginMessage = location.state?.message;

  return (
    <body className='login'>
    <div className='login'>
      <div className='logo-login'>
        <img src={logo} alt="logo" />
      </div>
      <div className='login-container'>
      <h2>
  Welcome! Login or{' '}
  <a onClick={handleRegister} style={{ color: '#0a4b79', cursor: "pointer", textDecoration: "underline" }}>
    Register
  </a> {' '}
  to get started!
</h2>
        {/* Error message display */}
        {message && (
          <div className="message" style={{ color: message.type === 'success' ? 'green' : 'red', textAlign: 'center' }}>
            {message.text}
          </div>
        )}
        {loginMessage && loginMessage.text && ( // Added check for loginMessage
          <div className="message" style={{ color: 'green', textAlign: 'center' }}>
            {loginMessage.text}
          </div>
        )}
        
        <form onSubmit={handleLogin} className='login-input'>
     
            <input 
              type="email" 
              placeholder="Email" 
              value={formData.email}
              onChange={(e) => setFormData(prev => ({ ...prev, email: e.target.value }))}
              required
            />
            <input 
              type="password" 
              placeholder="Password" 
              value={formData.password}
              onChange={(e) => setFormData(prev => ({ ...prev, password: e.target.value }))}
              required
            />
          
          <div className='login-button'>
            <button type='submit'>Login </button>
          </div>
        </form>
      </div>
    </div>
    </body>
  )
}

export default Login