# Next Steps

Here are some ideas for improving **Study-Bot**, ordered by priority:

## 1. Object Detection Performance
Find alternative methods to create and use custom object detection models that are more accurate and faster than the current implementation. 

This could involve using different model creation tools, or using a cloud computing service with access to GPUs with CUDA support to run the model we already have.

## 2. Concurrent Generation
Concurrent generation refers to the process of generating and playing audio from the Elevenlabs API while GPT is still generating its answer, all at the same time, significantly reducing the time it takes for **Study-Bot** to answer a question.

ElevenLabs created a [guide](https://elevenlabs.io/docs/api-reference/websockets#example-voice-streaming-using-elevenlabs-and-openai) on how to do this, but that method required the use of external software that would be difficult to bundle with **Study-Bot** for distribution. A proof of concept for a workaround was achieved in [concurrentGeneration.py](../Tests/AudioInteraction/concurrentGeneration.py) by using threads, and it is capable of answering a question in about 2-3 seconds, a major improvement over the current 13-18 seconds. 

However, adding this approach to into **Study-Bot** proved to be challenging. **Study-Bot**'s UI framework, Tkinter, is not thread-safe, and works best when running single-threaded synchronous tasks. This makes it difficult and probably impossible to implement concurrent generation.

This could be solved by using a different UI framework, such as PyQt, Kivy, or others. While this would require a complete rewrite of the UI, it may be the best way to achieve the lower response times that concurrent generation offers.

## 3. Interactive Quizzes
After studying a topic, users could take a quiz to test their knowledge. **Study-Bot** could enter into a 'quiz mode' where GPT could generate questions based on the source material, as well as provide feedback on the user's answers.

## 4. Interrupt Answers
Currently, after a question is made **Study-Bot** can only ignore all user input to avoid crashes when the answer is being generated or read out loud. Find a way to stop all threads when the user presses the question button while the answer is being processed, the answer is being read, or the program is suddenly closed.

## 5. Fine-tuning and Embeddings
Experiment with [embeddings](https://platform.openai.com/docs/guides/embeddings) or [fine tuning](https://platform.openai.com/docs/guides/fine-tuning) the GPT model with source material from reliable textbooks to improve the quality of the answers. 

Right now, **Study-Bot** recieves its source material in the first message as plain text, a quite rudimentary approach. Prompt """engineering""" was also used to achieve the desired behavior for this use case, but the constant updates to the models tend to change how closely the model follows the custom instructions.

## 6. Fun Facts and Follow-up Suggestions
Suggest learning about fun facts or new questions based on the user's last question.