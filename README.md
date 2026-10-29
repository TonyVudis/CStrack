# CS2 Tracker

A small Flask website for viewing CS2 player information and helpful map
lineups.

## Run locally

1. Install Python 3.
2. Create and activate a virtual environment:

   ```powershell
   python -m venv venv
   .\venv\Scripts\Activate.ps1
   ```

3. Install the dependencies:

   ```powershell
   pip install -r requirements.txt
   ```

4. Create a local `.env` file with your own configuration:

   ```text
   DB_PASSWORD=your-database-password
   DB_USER=your-database-user
   DB_HOST=your-database-host
   DB_NAME=your-database-name
   PORT=your-database-port
   Flash_key=replace-with-a-random-secret
   Leetify_API_key=your-leetify-key
   Steam_API_key=your-steam-key
   ```

   Use a database that has the tables required by the application.

5. Start the website:

   ```powershell
   python app.py
   ```

6. Open <http://127.0.0.1:5000> in a browser.

## Keep it safe

- Never commit `.env`, API keys, passwords, or other private configuration.
- Do not paste real credentials into this README or other public files.
- Use this built-in server for local testing only. Use a properly configured
  production server before making the site public.
- Keep API keys private and replace them if they are accidentally exposed.

## Main pages

- Home: search for a player
- Basics: CS2 basics
- Lineups: map lineup guides
- About: project information
