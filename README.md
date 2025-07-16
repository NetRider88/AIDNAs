# 🧬 AI DNAs Portfolio

A modern, responsive portfolio website showcasing AI development, automation solutions, and intelligent systems expertise.

## 🚀 Features

### **Core Portfolio**
- ✅ **Responsive Design** - Works perfectly on all devices
- ✅ **Project Showcase** - Live, In Progress, and Planned projects
- ✅ **Blog System** - AI automation insights and tutorials
- ✅ **Contact Forms** - Newsletter signup and contact messaging
- ✅ **Email Notifications** - Real-time alerts to john@aidnas.com

### **Technical Features**
- ✅ **Django REST API** - n8n automation integration
- ✅ **Google Analytics 4** - User behavior tracking
- ✅ **Social Sharing** - Enhanced blog post sharing
- ✅ **SEO Optimized** - Meta descriptions and structured data
- ✅ **Brand Separation** - Consistent "AI DNAs" branding

### **API Integration**
- ✅ **n8n Workflow Support** - Automated blog post creation
- ✅ **Token Authentication** - Secure API access
- ✅ **Bulk Operations** - Multiple post creation
- ✅ **Health Monitoring** - API status endpoints

## 🛠️ Technology Stack

- **Backend**: Django 5.2.4 + Python 3.12
- **Frontend**: Tailwind CSS + JavaScript
- **Database**: SQLite (development) / PostgreSQL (production)
- **Email**: Gmail SMTP with app passwords
- **Analytics**: Google Analytics 4
- **Deployment**: GCP VM ready

## 📦 Installation

### **Prerequisites**
```bash
# Python 3.12+
python --version

# Git
git --version
```

### **Local Development Setup**
```bash
# Clone the repository
git clone https://github.com/NetRider88/AIDNAs.git
cd AIDNAs

# Create virtual environment
python -m venv portfolio_env
source portfolio_env/bin/activate  # On Windows: portfolio_env\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Run development server
python manage.py runserver
```

### **Environment Configuration**
```bash
# Copy settings template
cp portfolio_site/settings.py portfolio_site/settings_local.py

# Edit settings_local.py with your configurations:
# - SECRET_KEY
# - EMAIL_HOST_PASSWORD (Gmail app password)
# - ALLOWED_HOSTS
# - DEBUG = True
```

## 🔧 Configuration

### **Email Setup**
1. Enable 2-Factor Authentication on Gmail
2. Generate App Password: Google Account → Security → App passwords
3. Update `EMAIL_HOST_PASSWORD` in settings
4. Test with newsletter signup

### **Analytics Setup**
1. Create GA4 account at [analytics.google.com](https://analytics.google.com)
2. Get Measurement ID (starts with G-)
3. Replace `G-DGBTY079VX` in `templates/base.html`
4. Deploy and start tracking

### **API Token Generation**
```bash
# Create API token for n8n integration
python manage.py create_api_token
```

## 📊 API Endpoints

### **Blog Automation API**
- `POST /api/v1/blog/create-post/` - Create new blog post
- `POST /api/v1/blog/bulk-create/` - Bulk post creation
- `GET /api/v1/blog/health/` - API health check
- `GET /api/v1/blog/stats/` - Blog statistics

### **Authentication**
- Token-based authentication
- Generated token: `7736327ffff7d1d22d4c9b5c1500d2d970b14689`

### **Example n8n Integration**
```bash
curl -X POST http://your-domain.com/api/v1/blog/create-post/ \
  -H "Authorization: Token 7736327ffff7d1d22d4c9b5c1500d2d970b14689" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "AI Automation Guide",
    "content": "Your blog content here...",
    "category": "Automation",
    "tags": "AI, n8n, automation"
  }'
```

## 🚀 Deployment

### **GCP VM Deployment**
```bash
# On your GCP VM
sudo apt update
sudo apt install python3 python3-pip nginx postgresql

# Clone repository
git clone https://github.com/NetRider88/AIDNAs.git
cd AIDNAs

# Setup virtual environment
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Configure production settings
# Edit portfolio_site/settings_production.py

# Run migrations
python manage.py migrate
python manage.py collectstatic

# Setup systemd service
sudo nano /etc/systemd/system/aidnas.service
sudo systemctl enable aidnas
sudo systemctl start aidnas

# Configure nginx
sudo nano /etc/nginx/sites-available/aidnas
sudo ln -s /etc/nginx/sites-available/aidnas /etc/nginx/sites-enabled/
sudo systemctl restart nginx
```

### **Production Settings**
```python
# portfolio_site/settings_production.py
DEBUG = False
ALLOWED_HOSTS = ['your-domain.com', 'your-vm-ip']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'aidnas_db',
        'USER': 'aidnas_user',
        'PASSWORD': 'secure_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

## 📁 Project Structure

```
AIDNAs/
├── portfolio_site/          # Django settings & configuration
├── main/                    # Core portfolio app
│   ├── models.py           # Profile, skills, testimonials
│   ├── views.py            # Home, about, contact pages
│   └── urls.py             # Main URL routing
├── projects/               # Project showcase app
│   ├── models.py           # Project & technology models
│   ├── views.py            # Project list & detail views
│   └── urls.py             # Project URL routing
├── blog/                   # Blog & API app
│   ├── models.py           # Blog post, category models
│   ├── views.py            # Blog views & API endpoints
│   ├── serializers.py      # REST API serializers
│   └── urls.py             # Blog & API URL routing
├── templates/              # HTML templates
│   ├── base.html           # Base template with analytics
│   ├── main/               # Home, about, contact templates
│   ├── projects/           # Project list & detail templates
│   └── blog/               # Blog templates
├── static/                 # CSS, JS, images
├── media/                  # User uploaded files
└── requirements.txt        # Python dependencies
```

## 🎯 Key Features Explained

### **Brand Separation**
- Static "AI DNAs" branding across all pages
- Personal identity separate from brand identity
- Consistent visual design

### **API Integration**
- RESTful API for n8n automation
- Token-based authentication
- Bulk operations support
- Health monitoring endpoints

### **Email System**
- Newsletter signup with notifications
- Contact form with email alerts
- Gmail SMTP integration
- Spam protection

### **Analytics Integration**
- Google Analytics 4 tracking
- Custom event tracking
- User behavior analysis
- Conversion goal tracking

## 🔒 Security Features

- ✅ CSRF protection on all forms
- ✅ SQL injection prevention
- ✅ XSS protection
- ✅ Secure file uploads
- ✅ Environment variable protection
- ✅ Production-ready settings

## 📈 Performance

- ✅ Optimized database queries
- ✅ Static file serving
- ✅ Image optimization
- ✅ Caching strategies
- ✅ Mobile-first responsive design

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 📞 Contact

- **Email**: john@aidnas.com
- **Website**: [AI DNAs Portfolio](https://your-domain.com)
- **GitHub**: [@NetRider88](https://github.com/NetRider88)

## 🙏 Acknowledgments

- Django community for the excellent framework
- Tailwind CSS for the beautiful design system
- Font Awesome for the icons
- Google Analytics for user insights

---

**Built with ❤️ by AI DNAs** 🧬 