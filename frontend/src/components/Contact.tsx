import React, { useState } from 'react';
import './Contact.css';

interface ContactForm {
  name: string;
  email: string;
  subject: string;
  message: string;
}

const Contact: React.FC = () => {
  const [formData, setFormData] = useState<ContactForm>({
    name: '',
    email: '',
    subject: '',
    message: ''
  });
  const [loading, setLoading] = useState(false);
  const [success, setSuccess] = useState(false);
  const [error, setError] = useState('');

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    });
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError('');
    setSuccess(false);

    try {
      const response = await fetch('/api/contact', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(formData),
      });

      if (!response.ok) {
        throw new Error('Failed to send message');
      }

      setSuccess(true);
      setFormData({ name: '', email: '', subject: '', message: '' });
    } catch (err) {
      setError('Failed to send message. Please try again.');
      console.error('Contact error:', err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <section className="contact section">
      <div className="contact-container">
        <h2 className="section-title">Get In Touch</h2>
        <p className="section-subtitle">
          Let's work together on your next project
        </p>

        <div className="contact-content">
          <div className="contact-info">
            <div className="card">
              <h3>Contact Information</h3>
              <div className="contact-item">
                <i className="fas fa-envelope"></i>
                <div>
                  <h4>Email</h4>
                  <p>your.email@example.com</p>
                </div>
              </div>
              
              <div className="contact-item">
                <i className="fas fa-phone"></i>
                <div>
                  <h4>Phone</h4>
                  <p>+1 (555) 123-4567</p>
                </div>
              </div>
              
              <div className="contact-item">
                <i className="fas fa-map-marker-alt"></i>
                <div>
                  <h4>Location</h4>
                  <p>San Francisco, CA</p>
                </div>
              </div>
            </div>

            <div className="card">
              <h3>Connect With Me</h3>
              <div className="social-links">
                <a href="https://linkedin.com/in/your-profile" target="_blank" rel="noopener noreferrer" className="social-link">
                  <i className="fab fa-linkedin"></i>
                  LinkedIn
                </a>
                <a href="https://github.com/yourusername" target="_blank" rel="noopener noreferrer" className="social-link">
                  <i className="fab fa-github"></i>
                  GitHub
                </a>
                <a href="https://twitter.com/yourusername" target="_blank" rel="noopener noreferrer" className="social-link">
                  <i className="fab fa-twitter"></i>
                  Twitter
                </a>
              </div>
            </div>
          </div>

          <div className="contact-form-container">
            <form onSubmit={handleSubmit} className="contact-form">
              <div className="form-group">
                <input
                  type="text"
                  name="name"
                  value={formData.name}
                  onChange={handleChange}
                  placeholder="Your Name"
                  required
                  className="form-input"
                />
              </div>
              
              <div className="form-group">
                <input
                  type="email"
                  name="email"
                  value={formData.email}
                  onChange={handleChange}
                  placeholder="Your Email"
                  required
                  className="form-input"
                />
              </div>
              
              <div className="form-group">
                <input
                  type="text"
                  name="subject"
                  value={formData.subject}
                  onChange={handleChange}
                  placeholder="Subject"
                  required
                  className="form-input"
                />
              </div>
              
              <div className="form-group">
                <textarea
                  name="message"
                  value={formData.message}
                  onChange={handleChange}
                  placeholder="Your Message"
                  required
                  rows={5}
                  className="form-textarea"
                ></textarea>
              </div>
              
              <button type="submit" className="btn" disabled={loading}>
                {loading ? (
                  <>
                    <i className="fas fa-spinner fa-spin"></i>
                    Sending...
                  </>
                ) : (
                  <>
                    <i className="fas fa-paper-plane"></i>
                    Send Message
                  </>
                )}
              </button>
            </form>

            {success && (
              <div className="success-message">
                <i className="fas fa-check-circle"></i>
                Message sent successfully! I'll get back to you soon.
              </div>
            )}

            {error && (
              <div className="error-message">
                <i className="fas fa-exclamation-triangle"></i>
                {error}
              </div>
            )}
          </div>
        </div>
      </div>
    </section>
  );
};

export default Contact;
