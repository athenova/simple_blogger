# **PythonSimpleBlogger library (simple_blogger)** #

This is simple library to make simple blog project with Python. 
The library is distributed under the MIT license and can be downloaded and used by anyone.

----------

## How to install ##

To install, you can use the command:

    pip3 install simple_blogger

Or download the repository from [GitHub](https://github.com/athenova/simple_blogger)

----------

## Initialization ##

Just start with a simple code. 

```python

blogger = simple_blogger.CommonBlogger(PUT-YOUR-TELEGRAM-PRIVATE-CHAT-ID-IN-HERE)
blogger.init_project()

```

It initalizes folder structure of your own blog project in the working directory.

### Blog topics ###

Find project ideas json-file in `files/ideas` folder. Fill it with topics and categories of your blog.

### Creating tasks ###

Call `push`.

```python

blogger.push()

```

It creates tasks json-file in `files` folder with dates of publications and prompts to AI that generate image and text for topics. 

### Adding Tasks ###

Put any json-file in `files/ideas` folder. It has to be idea-structured. You can put as many idea-files in idea folder as you want.

Call `revert` to put unhandled tasks back in backlog.

```python

blogger.revert()

```

Call `push` again. Now all backloged tasks and new ideas are in progress.

### Publication Review ###

Call `review` to send tommorow's publication to your private telegram channel.

```python

blogger.review()

```

### Publication ###

Call `send` to send today's publication to your public telegram channel.

```python

blogger.send()

```

**Note:** call `review` before `send` or call `send` with `image_gen`=`True`(*to produce image*) and `text_gen`=`True`(*to produce text*).
  
### Error handling ###

If something goes wrong method sends Exception text to your private telegram channel. 

### Default parameters ###

Library uses working directory name as project name and production telegram channel name by default.

### Environment variables ###

Library uses `dall-e-3` model to generate images and `deepseek-chat` to generate texts by default and sends publications to telegram channels.
It needs following environment variables:
- BLOGGER_BOT_TOKEN
- OPENAI_API_KEY
- DEEPSEEK_API_KEY
  

## From the developer ##

> There are(or will be) more examples of using this library in sibling repos on [GitHub](https://github.com/athenova/simple_blogger)