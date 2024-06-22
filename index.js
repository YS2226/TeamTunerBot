const express = require('express');
const { exec } = require('child_process');
const app = express();
const port = 3000;

app.use(express.json());

app.post('/send-message', (req, res) => {
  const { channelId, message } = req.body;

  if (!channelId || !message) {
    return res.status(400).send('Missing channelId or message');
  }

  exec(`python bot.py ${channelId} "${message}"`, (error, stdout, stderr) => { // 'python3' から 'python' に変更
    if (error) {
      console.error(`exec error: ${error}`);
      return res.status(500).send(`Error executing Python script: ${stderr}`);
    }
    console.log(`stdout: ${stdout}`);
    console.error(`stderr: ${stderr}`);
    res.send('Message sent');
  });
});

app.listen(port, () => {
  console.log(`Server is running on port ${port}`);
});
