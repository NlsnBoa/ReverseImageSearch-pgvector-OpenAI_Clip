// pages/api/upload.ts
import { IncomingForm, Fields, Files } from 'formidable';
import { promises as fs } from 'fs';
import path from 'path';
import { exec } from 'child_process';
import { NextApiRequest, NextApiResponse } from 'next';

export const config = {
  api: {
    bodyParser: false,
  },
};

export default async function handler(req: NextApiRequest, res: NextApiResponse) {
  const data = await new Promise<{ fields: Fields; files: Files }>((resolve, reject) => {
    const form = new IncomingForm();
    form.parse(req, (err, fields, files) => {
      if (err) return reject(err);
      resolve({ fields, files });
    });
  });

  // Assuming the file field is named 'image' and using any to avoid type errors for now
  // Ideally, you would create a more specific type that matches the expected structure
  const imagePath = data.files.image?.[0]?.filepath || '';

  // Path to your Python script
  const pythonScriptPath = path.resolve('reverse-search/image-search/image_search/main.py');
  // Construct the command to run your Python script using the uploaded image path
  const command = `poetry run "${pythonScriptPath}" "${imagePath}"`;

  exec(command, (error, stdout, stderr) => {
    if (error) {
      console.error(`exec error: ${error}`);
      return res.status(500).json({ message: 'Python script execution failed' });
    }
    console.log(`stdout: ${stdout}`);
    console.error(`stderr: ${stderr}`);

    // Process the output from your Python script here
    res.status(200).json({ message: 'Image processed', output: stdout });
  });
}
