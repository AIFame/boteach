# Boteach

## Idea

Is to bridge the educational disparities that arises in traditional classroom paradigms.

Students classified to

- Slow, Mid, Fast learners on the basis of their IQ and understand on the subject

## Roadmap

1. Demo App (v0.1)
    - A lecture video (7m-1hr)
    - AI is fed the lecture transcript
    - Students are allowed to listen to the video
    - Students can ask their doubts to the AI, and AI will answer in the ctxt of the video

2. Pre-MVP v0.2
    - Additionally, Students would be shown the lecture snip that explains the answer to their q.

   Outcome:
    1. We are not trying to replace human teachers
    2. We are trying to bridge the gap arises with students and human teachers.

3. MVP v0.3, v0.4
    - Expand our demo video -> 5 videos list
    - min: 90% accurate responses from AI in terms of lecture snip and prompt

4. MVP v0.5
    - Add support for all youtube videos

6. MVP v1.0
    - Role out RBAC (Role based Access control) to our beta users
    - Roles of users:
      i) Teacher- Upload video, and transcript. Evaluate
      ii) Learner- Search bar: to search for a lecture video and watch it and ask qs
7. MVP v1.2
    - Teacher Dashboard (see the video list, viewers etc)  Implementation: look for open source dashboards - PowerBI

8. MVP v1.3
    - AI Avatars powered by https://elevenlabs.io or https://studio.inworld.ai/
      ......

## TODO

- [ ]  Explore various youtube videos
- [ ] Separate assistants for every video
- [ ] Backup assistant ids in redis with respect to video