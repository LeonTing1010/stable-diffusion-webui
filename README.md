### Overview of AIGC Platform

The AIGC Platform meets the demands for AI model training and image generation, supports flexible resource management and scheduling, and can provide better services according to the demands of physical resources. It has main functions such as AI model training, AI image generation, elastic management, load balancing, and can also be integrated with external systems through API interfaces to achieve different computing tasks.

### Framework Structure of AIGC Platform

The platform is mainly composed of the following core modules:

- The Scheduling Management System is used to flexibly manage hardware resources such as GPUs. It can automatically adjust and optimize resource allocation according to the current computing resources to meet the demands of different computing tasks;
- AITP is mainly responsible for personalized model training and model service deployment. It can not only improve the performance of the model, but also make the model more stable;
- AIGC is mainly responsible for generating personalized scene pictures. It can generate accurate scene pictures that fit customer requirements according to different customer requirements;
- SS Support Service is responsible for adapting the interaction between external interfaces and the AI platform, including parsing MQ messages, docking distributed caches, and querying AIGC process information. It can effectively ensure the stable operation of the AI platform;
- The Monitoring Platform is responsible for monitoring the operation of each module, collecting real-time logs, real-time status monitoring, to ensure the normal operation of the AI platform and timely discover abnormalities;
- GW, as a gateway, mainly implements authentication and flow control of external access to ensure the safe operation of the AI platform.

![Untitled](https://s3-us-west-2.amazonaws.com/secure.notion-static.com/6f886446-a765-4173-9d7c-832225f06ad2/Untitled.png)
