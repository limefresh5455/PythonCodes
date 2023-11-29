import express, { Request, Response } from 'express';
import * as dotenv from 'dotenv';
import {extractTextFromPDF,chatResponse,fetchWikiPage} from './openaiem';
import path from 'path';
dotenv.config() 
const app = express();
const port = 5050;
app.listen(port, () => {
  console.log(`API listening on http://localhost:${port}`);
});
app.get('/', async (req, res) => {
  const indexPath = path.join(__dirname, 'index.html');
  var dirname = __dirname.split('/');
  dirname.pop();
  res.sendFile(dirname.join('/')+'/src/index.html');
});

app.get('/pdftovector', async(req: Request, res: Response) => {
    console.log("test")
    var dirname = __dirname.split('/');
    dirname.pop();
    console.log(dirname.join('/')+'/src/files/Web_Development_with_Node_Express.pdf');
    const ds:string = await extractTextFromPDF(dirname.join('/')+'/src/files/Web_Development_with_Node_Express.pdf');
    res.send("Hello");
});
app.get('/wikitovector', async(req: Request, res: Response) => {
  const wikidocs = await fetchWikiPage('https://en.wikipedia.org/wiki/History_of_Germany')

  // var dirname = __dirname.split('/');
  // dirname.pop();
  // console.log(dirname.join('/')+'/src/files/Web_Development_with_Node_Express.pdf');
  // const ds:string = await extractTextFromPDF(dirname.join('/')+'/src/files/Web_Development_with_Node_Express.pdf');
  // res.send("Hello");
  return "Hello"
});

//https://en.wikipedia.org/wiki/History_of_Germany


app.get('/api/chat', async (req, res) => {
 
  try {
    const messageParam = req.query.message;
    
    // Check if messageParam is a string or ParsedQs type
    let message: string = '';
    if (typeof messageParam === 'string') {
      // If it's a string, use it directly
      message = messageParam;
    } else if (Array.isArray(messageParam) && messageParam.length > 0 && typeof messageParam[0] === 'string') {
      // If it's an array, use the first element if it's a string
      message = messageParam[0];
    } else if (typeof messageParam === 'object' && messageParam !== null) {
      // If it's an object (ParsedQs), extract the first property's value if it's a string
      const keys = Object.keys(messageParam);
      if (keys.length > 0 && typeof messageParam[keys[0]] === 'string') {
        message = messageParam[keys[0]];
      }
    }

    const decodedString = decodeURIComponent(message);
    console.log(decodedString)
    const response = await chatResponse(decodedString);
    res.end(response)
    //res.send(response)
    //res.json({ response });
    //return response
  } catch (error) {
    console.error('Error processing message:', error);
    res.status(500).json({ error: 'Internal Server Error' });
  }
});
