# Personal Finance Dashboard

A comprehensive web-based expense tracking application built with Flask. Track expenses, manage budgets, visualize spending patterns, and export data - all with extensive educational documentation for junior developers.

## Features

### Core Functionality
- **Expense Management**: Add, edit, delete, and view expenses with categorization
- **Income Tracking**: Record and categorize income from multiple sources (Salary, Freelance, Investment, etc.)
- **Budget Tracking**: Set monthly budgets per category with visual progress indicators
- **Analytics & Charts**: Interactive pie, line, and bar charts using Chart.js
- **Filtering**: Filter by category, date range, or quick filters (this month, last 7 days, etc.)
- **CSV Export**: Export filtered data for external analysis
- **Dark Mode**: Smooth, flicker-free dark mode with persistent user preference
- **Responsive Design**: Works seamlessly on desktop, tablet, and mobile

### User Experience
- Clean, modern interface with smooth animations
- Real-time form validation (client and server-side)
- Loading states and clear error messages
- Accessibility compliant (WCAG 2.1)
- Keyboard navigation support
- Future date prevention on expense/income forms
- Character limits with visual feedback on text inputs

### Security
- SQL injection prevention (parameterized queries)
- XSS prevention (Jinja2 auto-escaping)
- Comprehensive input validation
- Secure session management

## Technology Stack

**Backend:**
- Python 3.8+
- Flask 3.0.0
- SQLite database

**Frontend:**
- HTML5, CSS3, JavaScript (ES6+)
- Chart.js 3.9.1 for data visualization

## Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Setup Instructions

1. **Clone or download the project**
   ```bash
   cd "path/to/Personal Finance Dashboard"
   ```

2. **Create and activate virtual environment**

   Windows:
   ```bash
   python -m venv venv
   venv\Scripts\activate
   ```

   Mac/Linux:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install Flask==3.0.0
   ```

4. **Run the application**
   ```bash
   python app.py
   ```

5. **Open in browser**

   Navigate to: `http://localhost:5000`

## Usage Guide

### Adding Expenses
1. Click "Add Expense" button
2. Fill in date, category, amount, and description (optional)
3. Submit to save

### Managing Budgets
1. Navigate to "Budgets" page
2. Select category and enter monthly limit
3. View progress bars showing spending vs. budget
4. Green = on track, Yellow = warning, Red = over budget

### Viewing Analytics
1. Navigate to "Analytics" page
2. View three interactive charts:
   - Pie chart: Spending breakdown by category
   - Line chart: Spending trends over time
   - Bar chart: Monthly comparisons

### Filtering & Export
1. Go to "View All Expenses"
2. Use filters to narrow results
3. Click "Export to CSV" to download filtered data

## Project Structure

```
├── app.py                  # Flask routes and request handling (1300+ lines)
├── database.py             # Database operations (1260+ lines)
├── models.py               # Data models and validation (1200+ lines)
├── finance.db              # SQLite database (auto-created, gitignored)
├── templates/              # Jinja2 HTML templates
│   ├── base.html           # Master template with dark mode support
│   ├── index.html          # Dashboard
│   ├── add_expense.html    # Add/edit expense form
│   ├── add_income.html     # Add/edit income form
│   ├── view_expenses.html  # Expense list with filters
│   ├── view_income.html    # Income list with filters
│   ├── analytics.html      # Charts and visualizations
│   └── budgets.html        # Budget management
├── static/
│   ├── css/style.css       # All styling with dark mode (1300+ lines)
│   └── js/main.js          # Client-side functionality (1200+ lines)
├── BUG_TRACKER.md          # Bug documentation and fixes
├── TESTING.md              # Complete testing guide
├── test_validation.py      # Automated validation tests
├── .gitignore              # Git ignore rules
└── LICENSE                 # MIT License

Total: ~10,000+ lines of code including extensive educational comments
```

## For Junior Developers

### Educational Value

This project is specifically designed as a learning resource. Every file includes extensive comments explaining:

- **What** the code does
- **Why** it's written this way
- **How** components interact
- **Best practices** and common mistakes
- **Alternative approaches**

### Learning Path

1. **Start with database.py**: Understand CRUD operations and SQL
2. **Read models.py**: Learn data structures and validation
3. **Study app.py**: Flask routing and request handling
4. **Review templates**: Jinja2 templating and HTML structure
5. **Explore style.css**: Modern CSS techniques (Grid, Flexbox, animations)
6. **Check main.js**: JavaScript patterns and DOM manipulation

### Key Concepts Covered

**Backend:**
- MVC architecture
- RESTful routing
- Database operations (SQLite)
- Form handling and validation
- Template rendering (Jinja2)
- Flash messages
- Error handling

**Frontend:**
- Semantic HTML5
- Responsive design (mobile-first)
- CSS animations and transitions
- Form validation (client & server)
- Chart.js integration
- Accessibility (WCAG 2.1)

**Security:**
- SQL injection prevention
- XSS prevention
- Input validation
- Secure coding practices

### Code Quality

- **DRY principle**: Reusable functions
- **KISS principle**: Simple, readable code
- **Comprehensive validation**: Client and server-side
- **Error handling**: Graceful degradation
- **Documentation**: Extensive inline comments

## Testing

### Automated Tests
Run validation test suite:
```bash
python test_validation.py
```

Expected: 13/13 tests pass (100%)

### Manual Testing
See `TESTING.md` for comprehensive test cases covering:
- All features
- Edge cases
- Browser compatibility
- Accessibility
- Performance
- Security

### Test Results
- ✅ SQL injection prevention
- ✅ XSS prevention
- ✅ Input validation (negative amounts, invalid dates, etc.)
- ✅ All CRUD operations
- ✅ Filtering and export
- ✅ Budget calculations
- ✅ Chart rendering

## Known Limitations

1. **Single user only** - No authentication system
2. **Local database** - Data stored locally, no cloud backup
3. **No recurring expenses** - Must manually enter repeated transactions
4. **Fixed categories** - Cannot create custom categories (7 expense categories, 8 income sources)

## Future Enhancements

**High Priority:**
- User authentication and multi-user support
- Cloud database option
- Recurring expense templates
- Mobile app

**Medium Priority:**
- Custom categories
- Budget alerts (email/SMS)
- PDF export
- Data backup/restore

**Low Priority:**
- Receipt image upload
- Tags and advanced search
- Predictive analytics
- Multi-currency support

## Troubleshooting

**Port 5000 already in use:**
- Change port in app.py: `app.run(port=5001)`

**CSS not loading:**
- Hard refresh: Ctrl+Shift+R (Windows) or Cmd+Shift+R (Mac)

**Database errors:**
- Delete `finance.db` and restart app to recreate

**Module not found:**
- Activate virtual environment
- Run: `pip install Flask==3.0.0`

**Windows encoding errors:**
- UTF-8 encoding fix already applied in test scripts

## Documentation Files

- **BUG_TRACKER.md**: All bugs discovered and how they were fixed
- **TESTING.md**: Comprehensive testing guide with checklists
- **test_validation.py**: Automated test suite for validation logic

## What I Learned

### Technical Skills
- Full-stack web development with Flask
- Database design and SQL queries
- Modern CSS (Grid, Flexbox, animations)
- JavaScript for interactivity
- Chart.js for data visualization
- Responsive design principles
- Accessibility standards (WCAG 2.1)

### Best Practices
- Client and server-side validation
- SQL injection and XSS prevention
- Error handling and user feedback
- Mobile-first responsive design
- Comprehensive documentation
- Systematic testing

### Key Takeaways
1. Validation is critical - never trust user input
2. Security by default - use parameterized queries, escape output
3. Comments explain why, not just what
4. Test edge cases early and often
5. Accessibility benefits all users
6. Documentation is for your future self

## Development Roadmap

### Week 1: Foundation ✅
- Project setup and database design
- Basic expense CRUD operations
- HTML templates and styling

### Week 2-3: Features ✅
- Category and date filtering
- Budget management
- Analytics with Chart.js
- CSV export

### Week 4: Polish ✅
- UI/UX improvements (animations, loading states)
- Comprehensive testing and bug fixes
- Complete documentation

## Security Notes

- Never commit `finance.db` (contains user data)
- Change `SECRET_KEY` in app.py before production
- Never use `debug=True` in production
- Always validate user input
- Use HTTPS in production deployment

## Contributing

This is a learning project, but contributions are welcome!

1. Fork the repository
2. Create a feature branch
3. Make changes with clear comments
4. Add tests for new features
5. Update documentation
6. Submit pull request

## License

MIT License - Feel free to use for learning and personal projects.

## Acknowledgments

**Technologies:**
- Flask framework and documentation
- Chart.js for beautiful charts
- SQLite for simple database management

**Learning Resources:**
- Flask documentation
- MDN Web Docs
- Real Python tutorials
- Stack Overflow community

## Contact

For issues or questions:
- Check inline code documentation (extensive comments in every file)
- Review TESTING.md for common problems
- Check BUG_TRACKER.md for known issues

## Project Stats

- **Lines of Code**: ~10,000+ (including educational comments)
- **Files**: 15+
- **Development Time**: 4 weeks
- **Features**: 10+ core features
- **Tests**: 13 automated validation tests
- **Documentation**: Comprehensive (README, TESTING, BUG_TRACKER)

---

**Built with focus on education, best practices, and real-world application.**

**Perfect for learning web development, building your portfolio, or actually tracking your expenses!**

*Start tracking your finances today! 💰*

---

*Last Updated: October 5, 2025*
