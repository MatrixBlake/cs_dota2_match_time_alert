# cs_dota2_match_time_alert
每日自动发送最近几天关注战队的比赛时间

## 如何使用
1. fork这个repo
2. 在gmail里create的一个自己的**App Passwords**（应用专用密码）
3. 在你的repo的**Settings → Secrets → Actions** → 添加repo secreats： `EMAIL_PASSWORD = 你的邮箱应用专用密码`
4. 在`fetch_and_mail.py`把发件人和收件人都改成自己的email
5. 选择性更改你关心的项目和战队，项目名在后面的url里要注意改写，战队名要和liquidpedia的url一致

**Note:**  
1. 注意对于每个战队都会去爬取一遍那个战队页面，如果战队页面的比赛时间没有更新，这里就不会爬取到。
2. 为了降低liquidpedia的压力，不建议每天爬取很多次，建议一天一次（在`.github/workflows/main.yaml`）里设置

---
## How to Use
1. Fork this repository.
2. Create your own **App Password** in Gmail.
3. In your repository, go to **Settings → Secrets → Actions** and add a repository secret:  `EMAIL_PASSWORD = your Gmail app password`
4. In `fetch_and_mail.py`, change the sender and receiver email addresses to your own.
5. Optionally, modify the projects and teams you care about. Make sure the project names in the URL are updated accordingly, and the team names match the URLs on Liquidpedia.


**Note:**  
1. The script scrapes each team’s page individually. If a team’s match schedule hasn’t been updated, it won’t be captured.  
2. To reduce load on Liquidpedia, it is not recommended to scrape multiple times per day. Running once per day is sufficient (set in `.github/workflows/main.yaml`).
