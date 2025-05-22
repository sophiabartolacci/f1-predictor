# F1 Standings Dashboard

A modern web application for displaying current Formula 1 standings, race results, and upcoming race information.

## Project Background

This application was developed during a 6 hour company-wide hackathon focused on leveraging Amazon Q for AI-assisted development. The challenge encouraged participants to explore how AI tools could accelerate development workflows and enhance productivity.

## Key Features

### Current Standings
- **Driver Standings**: View up-to-date driver championship standings with points
- **Constructor Standings**: Track team performance in the constructor championship
- **Visual Styling**: Team colors and position highlighting for better readability

### Race Information
- **Next Race Details**: Countdown timer to the upcoming Grand Prix with location and date
- **Last Race Results**: View podium finishers from the most recent race
- **Race Calendar**: Information about the current F1 season schedule

## Technology Stack

- **Backend**: Python with Flask API
- **Data Source**: FastF1 Python package
- **Frontend**: HTML, CSS, JavaScript 
- **Styling**: Custom CSS with F1 theming
- **Development Tools**: Amazon Q for AI-assisted development

## Challenges Encountered

- **API Selection**: Initially attempted to use OpenF1 API but encountered difficulties retrieving driver results and points for each race
- **Data Accuracy**: When switching to FastF1 API, faced challenges getting accurate driver standings, ultimately requiring hardcoded data
- **Constructor Points**: Successfully retrieved constructor standings but with minor point discrepancies
- **Race Results**: Struggled to get correct last race results from the API, had to hardcode the podium data
- **Date Handling**: Had difficulty with the date for the next race, though location and time were correctly retrieved

## Future Enhancements

- Race prediction features based on historical performance
- Historical race data and statistics
- Mobile-responsive design improvements

## Acknowledgements

This project uses the FastF1 API for Formula 1 data. All Formula 1 related data, images, and trademarks belong to their respective owners.