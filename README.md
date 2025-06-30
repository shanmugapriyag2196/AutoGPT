# AutoGPT - Role-Based AI Assistant Management System

## Overview

AutoGPT is a comprehensive web application that provides a role-based management system for creating, managing, and running custom AI assistants (AutoGPTs) across different business functions. The system supports multiple user roles with specific permissions and integrates with OpenAI's GPT models for intelligent text processing and analysis.

## Features

### Authentication & User Management
- **Multi-role user system** with Admin, Manager, HR, Developer, Resourcing, Operations, and Marketing roles
- **Secure login/logout** functionality with session management
- **Password recovery** system with email verification
- **User profile management** with role-based permissions
- **Account activation/deactivation** capabilities

### Business Function Support
- **Sales** - Sales-related AI assistants
- **HR** - Human Resources AI assistants  
- **Development** - Software development AI assistants
- **Resourcing** - Resource management AI assistants
- **Operations** - Operational AI assistants
- **Marketing** - Marketing-focused AI assistants

### AutoGPT Management
- **Create custom AutoGPTs** with specific prompts and business functions
- **Template file upload** support for structured data processing
- **Version control** for AutoGPT configurations
- **Help text integration** for user guidance
- **Status management** (Active/Inactive)

### 💬 AI Processing Capabilities
- **Text processing** with OpenAI GPT-4 integration
- **File upload and analysis** functionality
- **Conversation memory** for contextual responses
- **Structured data extraction** from various input formats
- **Real-time AI responses** with formatted output

### 📊 Dashboard & Analytics
- **Role-based dashboard** with function-specific access
- **Business function icons** with intuitive navigation
- **Response history** tracking and viewing
- **User activity monitoring**

## Technology Stack

### Backend
- **Flask 2.2.5** - Web framework
- **SQLAlchemy 3.1.1** - Database ORM
- **Flask-Migrate 4.0.5** - Database migrations
- **Flask-Mail 0.9.1** - Email functionality
- **bcrypt 4.0.1** - Password hashing

### AI & ML
- **OpenAI 1.14.1** - GPT-4 API integration
- **LangChain 0.0.350** - AI/LLM framework
- **sentence-transformers** - Text embedding
- **pinecone** - Vector database (optional)

### Database
- **SQLite** - Primary database with multiple tables:
  - `autogpt1.db` - AutoGPT configurations
  - `user4.db` - User management
  - `user2.db` - Recovery email management
  - `responses.db` - AI response history

### Frontend
- **HTML5/CSS3** - Modern responsive design
- **JavaScript** - Interactive functionality
- **Font Awesome** - Icon library
- **Bootstrap-inspired** styling