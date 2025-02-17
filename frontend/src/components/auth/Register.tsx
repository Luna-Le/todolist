import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { showMessage } from '../../utils/messages'
import type { MessageType } from '../../types'
import logo from "../../assets/logo.png"
import './Register.css'

function Register() {
  const [formData, setFormData] = useState({
    email: '',
    password: ''
  });
  const [message, setMessage] = useState({
    text: '',
    type: null as MessageType
  });
  const navigate = useNavigate();

  const handleRegister = async (e: React.FormEvent) => {
    e.preventDefault();
    
    try {
        const response = await fetch('https://todolistnow.com/users/', { 
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
            },
            body: JSON.stringify({
              email: formData.email,
              password: formData.password
            }),
        });

        const data = await response.json()

        if (response.ok){
            // #delay for 10secs
            showMessage('Registration successful! Redirecting you to login.', 'success', setMessage);
            setTimeout(() => {navigate("/", { state: { message: { text: 'Registration successful! Please login.', type: 'success' } } });}, 1000);
        }else{
            showMessage(data.detail || 'Registration failed', 'error', setMessage);
            
        }
    }catch (error) {
            console.error('Registration error:', error);
            showMessage('Registration failed. Please try again.', 'error', setMessage);
            alert('Registration failed')
          }
        }




 

  return (
    <body className="register">
    <div className='register'>
    <div className='logo-register'>
      <img src={logo} alt="logo" />
    </div>
    <div className='register-container'>
    <h2>
Welcome! Register to get started! </h2>
      {/* Error message display */}
      {message.text && (
        <div className={`message ${message.type}`} style={{ 
          color: message.type === 'success' ? 'green' : 'red',
          textAlign: 'center',
        
        }}>
          {message.text}
        </div>
      )}
      
      <form onSubmit={handleRegister} className='register-input'>
     
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
    
        <div className='register-button'>
          <button type='submit'>Register</button>
          <button onClick={() => navigate('/')}>Back to Login</button>
        </div>
      </form>
    </div>
  </div>
  </body>
)
}


export default Register