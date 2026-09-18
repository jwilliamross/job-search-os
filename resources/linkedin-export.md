# Exporting LinkedIn connections (for the outreach skill)

LinkedIn's API gives Claude no access to connections, so the CSV export is the source.

1. On desktop, click your photo (top right) → **Settings & Privacy**.
2. Left menu: **Data privacy** → under "How LinkedIn uses your data" click
   **Get a copy of your data**.
3. Choose **"Want something in particular?"** and tick **Connections** only. (The full
   archive works too but takes longer and is bigger.)
4. **Request archive**. LinkedIn emails a download link, usually within 10 minutes for the
   connections-only option (up to 24 hours for the full archive).
5. Download the ZIP, unzip, find `Connections.csv`. Columns: First Name, Last Name, URL,
   Email Address (only for people who allow it), Company, Position, Connected On. The file
   starts with three note lines before the header; Claude handles that.
6. Upload `Connections.csv` in chat. Claude will save it to `profile/network/` (private repo)
   and build `profile/network/finance-contacts.md`: everyone at a bank, fund, trading shop,
   relevant employer, plus alumni of your school and high school.

Re-export every couple of months; the outreach skill reads the latest file.
