<body>
  <div align="center">
    <img src="https://github.com/yuki-shi/gnight/blob/main/assets/picmix.com_2400899.gif">
    <h1>gnight ~ simplest google sheets API wrapper</h1>
    <p>read and write google sheets files from and with dataframes</p>
  </div>
  <h2>:robot: use cases</h2>
  <h2>:steam_locomotive: usage</h2>
  <h3>activate sheets API</h3>
    <p>activate google sheet's API on a google cloud plataform project by <a href="https://developers.google.com/sheets/api/quickstart/python">clicking here</a>.</p>
  <h3>create a service account</h3>
  <p><b>(1)</b> on the <i>IAM & admin</i> section, under <i>service accounts</i> (or by <a href="https://console.cloud.google.com/iam-admin/serviceaccounts">clicking here</a>) create a new service account </p>
  <img src="https://github.com/yuki-shi/gnight/blob/main/assets/create_account.png">
  <br>
  <p><b>(2)</b> fill in a name (ID) for your service account</p>
  <img src="https://github.com/yuki-shi/gnight/blob/main/assets/create_account2.png">
  <br>
  <p><b>(3)</b> you'll be returned to the previous screen. there'll be a new service account on the list, click on it</p>
  <img src="https://github.com/yuki-shi/gnight/blob/main/assets/creat_account3.png">
  <br>
  <p><b>(4)</b> select <i>keys</i> then <i>add key</i> and click on <i>create new key</i>. when prompted on the key type, select JSON.</p>
  <img src="https://github.com/yuki-shi/gnight/blob/main/assets/create_key.png">
  <br>
  <p><b>(5)</b> the key will be downloaded. store it on the same folder of the project or anywhere easy to remember. you may open it to find your service account e-mail, copy it.</p>
  <img src="https://github.com/yuki-shi/gnight/blob/main/assets/create_key2.png">
  <h3>share spreadsheet with service account</h3>
  <p>open a google sheets file and share it with the service account e-mail you just copied.</p>
  <img src="https://github.com/yuki-shi/gnight/blob/main/assets/share.jpg">
  <h3>install requirements</h3>
  
  ```bash
  $ pip install -r requirements.txt
  ```
  
  <h3>run</h3>
  
  ```bash
  
  ```
  
  <h2>:jack_o_lantern: technology</h2>
  python.
</body>
