## Capstone Project II
PRJ63504
```
AgriSense: IoT-Driven Early Warning System for
```
Weather and Pest Risk Management
Lee Zhen Jen
```
(ID0363642)
```
SCHOOL OF COMPUTER SCIENCE
```
BACHELOR OF SOFTWARE ENGINEERING (HONS)
```
APRIL 2025 [PART 1]
```
SUPERVISOR: Dr Saliyah
```
1.0 Project Proposal..................................................................................................................4
1.1 General Information....................................................................................................... 4
1.2 Executive Summary....................................................................................................... 4
1.3 Project Purpose...............................................................................................................5
1.3.1 Problem Statement..............................................................................................5
1.3.2 Project Objectives............................................................................................... 6
1.3.3 Functionalities..................................................................................................... 6
1.4 Assumptions................................................................................................................... 7
1.5 Project Description......................................................................................................... 7
1.5.1 Project Description.............................................................................................. 7
1.5.2 Scope.................................................................................................................. 8
1.5.3 Summary of Milestones and Deliverables........................................................... 9
1.6 Project Organization.....................................................................................................10
1.6.1 Project Organization Chart................................................................................ 10
1.6.2 Organization Description................................................................................... 10
1.6.3 Roles and Responsibilities.................................................................................11
2.0 Literature Review.............................................................................................................13
2.1 Introduction.................................................................................................................. 13
2.2 Existing System............................................................................................................13
2.2.1 Case Study 1: Smart Paddy Rice Production Framework.................................13
2.2.2 Case Study 2: IoT-Agro Coffee Farm System................................................... 14
2.2.3 Case Study 3: Smart Tomato Monitoring System..............................................14
2.3 Internet of Things....................................................................................................... 16
2.3.1 Layered Architecture Framework...................................................................... 16
2.3.2 Sensor Technologies and Selection Considerations......................................... 17
2.3.3 Communication Technology Selection.............................................................. 18
2.3.4 Platform Integration and Simulation.................................................................. 18
2.3.5 Simulation Platforms for Real-Time IoT Environments......................................19
2.3.6 Regional Context and Adoption Barriers........................................................... 19
2.3.7 Conclusion.........................................................................................................20
2.4 Cloud Platform............................................................................................................. 21
2.4.1 Cloud Service Models in Agricultural Applications............................................ 21
2.4.2 Major Cloud Platform Implementations in Agriculture....................................... 22
```
2.4.2.1 Amazon Web Services (AWS)..................................................................22
```
2.4.2.2 Microsoft Azure.........................................................................................23
```
2.4.2.3 Google Cloud Platform (GCP).................................................................. 24
```
2.4.3 Cloud Platform Selection...................................................................................24
2.4.4 Conclusion.........................................................................................................25
2.5 Database....................................................................................................................... 26
2.5.1 Single Database Architecture............................................................................26
2.5.2 Relational Database Technologies in Agricultural Applications.........................26
2.5.2.1 PostgreSQL.............................................................................................. 26
2.5.2.2 MySQL......................................................................................................27
1
2.5.2.3 SQL Server...............................................................................................28
2.5.3 Relational Database Selection.......................................................................... 28
2.5.4 Conclusion.........................................................................................................29
2.6 Machine Learning........................................................................................................ 30
2.6.1 Weather Prediction Model................................................................................. 30
2.6.1.1 Regression-Based Approaches................................................................30
2.6.1.2 Classification-Based Approaches.............................................................30
2.6.1.3 Model Selection Rationale........................................................................31
2.6.2 Pest Computer Vision........................................................................................32
2.6.2.1 Traditional vs Deep Learning Approaches............................................... 32
2.6.2.2 Real-Time Detection Systems.................................................................. 32
2.6.2.3 Model Selection Rationale........................................................................33
2.6.3 Conclusion.........................................................................................................33
2.7 Mobile Application...................................................................................................... 34
2.7.1 User Interface Design........................................................................................34
2.7.1.1 Design Challenges in Agricultural Contexts............................................. 34
2.7.1.2 Essential Design Principles and Best Practices....................................... 34
2.7.1.3 Analysis of Existing Agricultural Applications........................................... 35
2.7.2 User Experience................................................................................................37
2.7.2.1 Key UX Factors........................................................................................ 37
2.7.2.2 UX Design Implications for Agricultural Applications................................37
2.7.3 Mobile Frontend Development Framework Selection....................................... 38
2.7.3.1 Cross-Platform Framework Comparison.................................................. 38
2.7.3.2 Programming Language Considerations.................................................. 39
2.7.3.3 Framework Selection Rationale................................................................39
2.7.4 Conclusion.........................................................................................................39
2.8 System Backend........................................................................................................... 41
2.8.1 Architectural Pattern Analysis........................................................................... 41
2.8.2 Backend Technology Selection......................................................................... 43
2.8.2.1 Python with Flask..................................................................................... 43
2.8.2.2 JavaScript with Node.js............................................................................ 43
2.8.2.3 Java with Spring Boot...............................................................................44
2.8.2.2 Backend Technology Selection Rationale................................................ 44
2.8.3 Data Ingestion and API Design......................................................................... 44
2.8.4 Conclusion.........................................................................................................46
2.8 Conclusion....................................................................................................................47
3.0 System Analysis.............................................................................................................48
3.1 Introduction.................................................................................................................48
3.2 Proposed System....................................................................................................... 48
3.2.1 System Overview.............................................................................................. 48
3.2.2 System Architecture.......................................................................................... 49
3.2.2.1 Device Simulation Layer - Wokwi Platform...............................................50
3.2.2.2 Perception Layer - Physical Sensors and Devices...................................50
3.2.2.3 Networking Layer - Communication Infrastructure................................... 51
2
3.2.2.4 Cloud Data Simulation - Ubidots STEM Platform..................................... 51
3.2.2.5 Middleware Layer - Azure Cloud Services............................................... 52
3.2.2.6 Backend Service Architecture.................................................................. 53
3.2.2.7 Key Backend Responsibilities.................................................................. 53
3.2.2.8 Application Layer - User Interfaces.......................................................... 55
3.2.2.9 System Benefits and Future Considerations............................................ 55
3.3 Use Case Diagram..................................................................................................... 57
3.3.1 Use Case Specification..................................................................................... 60
3.4 Data Flow Diagram.....................................................................................................78
3.4.1 Data Sources and Input Processing..................................................................78
3.4.2 Machine Learning and Analytics Pipeline..........................................................79
3.4.3 User Interface and Interaction Layer................................................................. 79
3.4.4 Information Flow and Data Management.......................................................... 80
3.4.5 Decision Support Capabilities........................................................................... 80
3.4.6 System Integration and Scalability.................................................................... 81
3.5 SWOT Analysis.......................................................................................................... 82
4.0 System Design............................................................................................................... 84
4.1 Introduction.................................................................................................................84
4.2 Interface Design......................................................................................................... 84
4.3 Workflow of Proposed System................................................................................... 99
4.4 UML Class Diagram................................................................................................. 101
4.5 UML State Diagram..................................................................................................103
4.5.1 User Session Lifecycle.................................................................................... 103
4.5.2 User Registration Flow.................................................................................... 104
4.5.3 Dashboard Interaction..................................................................................... 105
4.5.4 IoT Data Handling Simulation..........................................................................106
4.5.5 Admin Management........................................................................................ 107
4.6 UML Sequence Diagram.......................................................................................... 108
4.6.1 User Login Flow.............................................................................................. 108
4.6.2 Upload Pest Image and Get AI Feedback.......................................................109
4.6.3 Viewing Dashboard Data and Alert..................................................................110
4.6.4 IoT Simulation Data Flow.................................................................................112
4.6.5 Admin Managing User and Settings................................................................ 113
4.7 Test Plan...................................................................................................................114
4.7.1 Levels of Testing.............................................................................................. 114
4.8 Design Test Scenario................................................................................................115
4.8.1 API Endpoint Testing....................................................................................... 115
4.8.2 Database Operations.......................................................................................115
4.8.3 Cloud Service Integration................................................................................ 115
4.8.4 Performance and Scalability............................................................................ 116
4.8.5 Security Testing............................................................................................... 116
Reference............................................................................................................................ 117
3
Table of Figures
Figure 1: Layered Architecture of IoT Systems
Figure 2: Collaboration between Big Tech companies and Cloud Platform
Figure 3: Monitor Panel Screen
Figure 4: Agrio User Interface
Figure 5: Layered Architecture
Figure 6: REST API
Figure 7: System Architecture Diagram of AgriSense
Figure 8: Use Case Diagram of AgriSense
Figure 9: Data Flow Diagram for AgriSense
Figure 10: User Interface of AgriSense
Figure 11: Splash Screen, Sign Up Screen, and Login Screen
Figure 12: Password Reset Flow Screens
Figure 13: Home Screen, Settings Screen, and Notification Screen
Figure 14: Farm Management Screen, Import Dataset Screen, AI Chatbot Screen
Figure 15: Weather Details Screens
Figure 16: Pest Alerts and Details Screen, Control Recommendation Screen
Figure 17: Report Pest Screens
Figure 18: Workflow of AgriSense
Figure 19: Class Diagram of AgriSense
Figure 20: State Diagram - User Session Lifecycle
Figure 21: State Diagram - User Registration Flow
Figure 22: State Diagram - Dashboard Interaction
Figure 23: State Diagram - IoT Data Handling Simulation
Figure 24: State Diagram: Admin Management
Figure 25: Sequence Diagram - User Login Flow
Figure 26: Sequence Diagram - Upload Pest Image and Get AI Feedback
Figure 27: Sequence Diagram - Viewing Dashboard Data and Alert
Figure 28: Sequence Diagram - IoT Simulation Data Flow
Figure 29: Sequence Diagram - Admin Managing User and Settings
4
Table of Tables
Table 1: Cloud Platform Comparison Table
Table 2: Relational Database Management System Comparison Table
Table 3: SWOT Analysis of AgriSense
5
1.0 Project Proposal
1.1 General Information
Points of Contact
List the principal individuals who may be contacted for information regarding the project.
Position Name Phone Number E-mail
Supervisor Dr.Saliyah Kahar +60129264258 saliyah.kahar@taylors.edu.my
Project Members
Lee Zhen Jen +60123990214 0363642@sd.taylors.edu.my
Peng Wei Keat +601151068202 weikeat.peng@sd.taylors.edu.my
Pang Zen An +60178213226 zenan.pang@sd.taylors.edu.my
Wong Cheng Ze +60187604475 0363305@sd.taylors.edu.my
Wong Zi Jun +60126782341 0363444@sd.taylors.edu.my
1.2 Executive Summary
The project aims to create AgriSense, a mobile application that serves as an IoT-based early
warning system for weather and pests to solve the inefficiency in the agricultural risk
management faced by the Malaysian farmers. The document introduces the objectives of the
system such as, centralization of the real-time weather monitoring, visual detection of pests
based on image analysis, and recommendations to minimize crop loss. AgriSense will help
farmers to make data-driven decisions that will allow them to react to environmental and
pest-related challenges proactively without the overuse of reactive pesticides.
The main goals of the project include offering user-friendly applications with the ability to
predict weather anomalies with the help of machine learning and a computer vision model with
deep learning to detect pest presence, based on a combination of IoT sensor and image data, to
6
allow timely warning and contingency planning. AgriSense would have a smooth dashboard of
the present weather, past trends, forecasting, pest detection, and AI chatbot as an advisory friend
as its key features. The proposal gives the details on how the workflows of the suggested
functions resolve the major hindrances of weather uncertainty, delayed pest identification, and
disjointed data. There is also a time based project plan and agreement of collaboration with the
agricultural institutions in the proposal.
1.3 Project Purpose
1.3.1 Problem Statement
1. Unpredictable Weather Conditions Affect Farming Decisions
The weather in Malaysia is not constant and it can rain at any time or it can be dry for a
long time. This complicates planning such processes as watering or fertilizing crops by
```
farmers (Tan et al., 2021). Lack of precise, real-time weather information makes many
```
farmers resort to guessing, which may occasionally lead to low crop productions and
even crop failure. Although IoT devices can be used to monitor and predict weather, not
all farms have access to such technologies.
2. Lack of Early Detection of Pest Infestations
Farmers usually find out about pest infestations by the time they have caused visible
damages, and this causes them to apply pesticides late and lose more crops. Research has
indicated that the current systems are more inclined to soil and weather tracking, instead
```
of providing the majority of farmers with viable real-time monitoring systems (Dasari et
```
```
al., 2024). Consequently, farmers have remained dependent on reactive application of
```
pesticides when crops have already been damaged, and increasing loss and environmental
degradation.
3. Limited Accessibility to Real-time Decision Support
In Malaysia and especially in the rural areas, farmers are confronted with enormous
difficulties in accessing real-time, intuitive systems that can process highly complicated
data concerning farming into simple, executable advice on how to manage risks including
unpredictable weather, disease outbreaks, and pests.
7
1.3.2 Project Objectives
1. To design a system that uses IoT-based environmental data to monitor and develop a
machine learning model to predict sudden weather changes, helping farmers make timely
and informed decisions.
2. To develop a deep learning–based computer vision model that detects the presence of
harmful agricultural pests from crop images, enabling timely alerts and supporting
proactive pest control efforts.
3. To create an integrated, resource-efficient, easy-to-use mobile platform that combines
multiple data sources and presents clear insights to help farmers adopt smart farming with
minimal technical knowledge.
1.3.3 Functionalities
No. Proposed Functionality Problems Solved/ Opportunities
1 Real-Time Alerts
```
Unpredictable Weather Conditions Affect Farming Decisions (1)
```
```
Lack of Early Detection of Pest Infestations (2)
```
```
Limited Accessibility to Real-time Decision Support (3)
```
2 Recommend Actions
```
Unpredictable Weather Conditions Affect Farming Decisions (1)
```
```
Lack of Early Detection of Pest Infestations (2)
```
```
Limited Accessibility to Real-time Decision Support (3)
```
3
Display Real-Time
Weather Conditions
```
Unpredictable Weather Conditions Affect Farming Decisions (1)
```
4
Display Weather
Forecast
```
Unpredictable Weather Conditions Affect Farming Decisions (1)
```
5
Display Historical
Weather Trends
```
Unpredictable Weather Conditions Affect Farming Decisions (1)
```
7
Display Pest Detection
Alerts and Details
```
Lack of Early Detection of Pest Infestations (2)
```
```
8 AI Chat Bot Limited Accessibility to Real-time Decision Support (3)
```
```
9 Dataset Import Limited Accessibility to Real-time Decision Support (3)
```
```
10 Dashboard Limited Accessibility to Real-time Decision Support (3)
```
8
1.4 Assumptions
● Assume that all collected data comply with Malaysian data-privacy regulations and won’t
store any personally identifiable information.
● Assume that all software used is properly licensed to avoid legal or support issues.
● Assume that all users of this mobile application have access to a stable internet and the
necessary technology to use the system efficiently.
● Assume the IoT sensors can be integrated into the system.
1.5 Project Description
1.5.1 Project Description
The Malaysian agricultural industry, which is the driving factor of the national economy and food
```
safety, is increasingly jeopardized by climate uncertainty and the loss of crops to pests (Muhamad
```
```
& Abdul Rahman, 2022). There is unpredictable weather, rains, droughts, late detection of pests
```
especially on smallholder farmers in rural areas which leads to reactive measures like overuse of
pesticides that add up to the cost and damage the environment. Inability to access real time
decision-support systems when majority of them use manual observations and outdated or
inaccurate data that may result in poor decision making and low yields.
AgriSense is a mobile application available in both Android and iOS, the purpose of the
application is to empower the Malaysian farmers with real-time weather forecasts and visual pest
detection alerts. AgriSense uses historical weather data based on machine learning models trained
using IoT sensor data available at various sources like Malaysian Meteorological Department and
MARDI to forecast weather conditions such as heavy rainfall and dry spells. Simultaneously, the
app integrates a computer vision model using deep learning to recognize dangerous agricultural
```
pests in the images of a crop field and detect them early to intervene in time (Karar et al., 2021).
```
Recommendations are sent to farmers in the form of in-app notifications, allowing them to take
proactive actions.
AgriSense is developed with the use of simulated IoT and image data, but is planned to be
```
deployed in the future with physical sensor hardwares (environmental sensors and smart cameras)
```
that farmers will be able to install in the field. The platform targets smallholder farms in Malaysia
9
for early testing and validation. The end result will be to minimize sudden crop losses, maximize
the use of inputs and offer a flexible, scalable solution that farmers can implement over time,
based on available infrastructure and resources.
1.5.2 Scope
AgriSense will only be deployed on Android and iOS. The system’s predictive models and
datasets will be tailored to suit the agricultural context in Malaysia, allowing for more accurate
weather prediction and pest detection.
```
Primary roles (Stakeholders):
```
1. Project Team - Responsible for developing and testing the application
2. Users - Farmers and agricultural agencies
The following types of data will be used for processing:
1. Time
2. Temperature (°C)
3. Relative Humidity (%)
4. Rain (mm)
5. Wind Speed (km/h)
6. Shortwave Solar Radiation GHI (W/ )𝑚2
7. Mean Soil Temperature (0–7 cm depth, °C)
8. Mean Soil Moisture (0–7 cm depth, / )𝑚3 𝑚3
9. Weather Code
10. Agricultural Pest Images
The following features will be delivered:
1. Real-Time Alerts
2. Recommend Actions
3. Display Real-Time Weather Conditions
4. Display Historical Weather Trends
5. Display Potential Risks - Weather
6. Pest Detection Alerts
10
7. Display Weather Forecast
8. AI Chat Bot
9. Dataset Import
10. Dashboard
The project shall not include the following features:
1. Deployment of physical IoT sensors or hardware.
2. Data acquisition from IoT sensor device
3. Development of web or desktop applications.
4. Multilingual support.
1.5.3 Summary of Milestones and Deliverables
Milestone
No.
Milestone Person
Responsible
Expected Duration
```
(days)
```
```
001 Project ProposalFinalization All 16 May – 23 May(7 days)
```
```
002 IoT Device Research& RequirementsLee Zhen Jen,Peng Wei Keat24 May – 30 May(7 days)
```
```
003 IoT Device Design &PrototypingLee Zhen Jen,Peng Wei Keat31 May – 20 June(21 days)
```
```
004 Backend ArchitectureDesign Lee Zhen Jen 21 June – 25 June(5 days)
```
```
005 Backend & DatabaseDevelopmentLee Zhen Jen,Peng Wei Keat26 June – 9 July(14 days)
```
006
Machine Learning
Data Collection &
Preprocessing
Pang Zen An,
Wong Cheng Ze
10 July – 16 July
```
(7 days)
```
007
Machine Learning
Model Training &
Optimization
Pang Zen An,
Wong Cheng Ze
17 July – 26 July
```
(10 days)
```
```
008 Mobile FrontendUI/UX DesignWong Zi Jun,Pang Zen An27 July – 7 August(12 days)
```
```
009 Mobile FrontendDevelopmentWong Zi Jun,Pang Zen An10 February – 19 February(10 days)
```
```
010 API Development &Integration Wong Cheng Ze 20 February – 27 February(8 days)
```
```
011 System Integration Wong Cheng Ze 28 February – 9 March(10 days)
```
```
012 Testing & Debugging All 10 March – 16 March(7 days)
```
```
013 Final Deployment &Documentation All 17 March – 23 March(7 days)
```
11
1.6 Project Organization
1.6.1 Project Organization Chart
1.6.2 Organization Description
AgriSense is a team project by a group of students of Taylor s University under the guidance of
Dr. Saliyah Kahar. The project's mission is to build an early-warning system for smallholder
farmers that combines IoT sensors and machine learning to forecast weather anomalies and deep
learning to identify pests based on real-time environmental data.
The project supervisor is Dr. Saliyah Kahar. She is in charge and supervises the progress of the
development of the project and gives advice on technical and research aspects in order to ensure
academic excellence. She also gives advice on project requirements to make sure that the
platform is relevant to the real world agricultural issues as well as the needs of target users,
including smallholder farmers in Selangor.
12
The project team consists of five final-year students, each assigned specific responsibilities:
● Lee Zhen Jen – Project Manager, Backend Developer, Cloud Engineer
● Peng Wei Keat – Database Engineer Developer, Data Engineer, IoT Engineer
● Pang Zen An – Machine Learning Developer, UI/UX Designer
● Wong Cheng Ze – Machine Learning Developer, API Developer
● Wong Zi Jun – Mobile Frontend Developer
This structure ensures a clear line of authority, with the project supervisor overseeing the team
and all members reporting to the project manager. The division of roles allows efficient
collaboration across system architecture, IoT integration, machine learning, mobile development,
and data management, establishing a strong foundation for real-world implementation in
agriculture.
1.6.3 Roles and Responsibilities
Name Roles Responsibilities
Dr. Saliyah Kahar Project Supervisor
To provide technical and academic guidance
throughout the project. To oversee progress,
ensure deliverables meet academic standards,
and ensure the project addresses real-world
agricultural challenges.
Lee Zhen Jen
Project Manager,
Backend Developer,
Cloud Engineer
Leads project planning and coordination,
manages team progress, develops backend
services for the mobile app, and handles cloud
deployment and infrastructure setup.
Peng Wei Keat
Database Engineer
Developer, Data
Engineer, IoT
Engineer
Designs and manages the project’s database,
processes incoming data from IoT devices, and
ensures smooth integration of sensor data into
the system.
Pang Zen An
Machine Learning
Developer, UI/UX
Designer
Builds and trains machine learning models for
pest and weather prediction, and designs the
mobile app’s user interface to ensure a smooth
user experience.
13
Wong Cheng Ze
Machine Learning
Developer, API
Developer
Develops machine learning models and
implements APIs to deliver predictions and
recommendations to the mobile app.
Wong Zi Jun
Mobile Frontend
Developer
To design and implement the user interface for
the mobile app. To ensure the platform is user
friendly and accessible for farmers with limited
technical background.
14
2.0 Literature Review
2.1 Introduction
The use of smart technologies in the agricultural sector is rapidly changing the traditional
farming pattern into data-driven and precision-based systems. The most recent developments
```
in the Internet of Things (IoT), machine learning, and cloud computing have made real-time
```
monitoring, predictive analytics, and automation of agricultural processes possible. This
literature review delves into the important technological frameworks and case studies that
demonstrate the manner in which such innovations are improving agricultural productivity,
sustainability and decision-making particularly in resource-limited settings such as rural
Malaysia. This literature review emphasises more in depth into the backend and cloud
infrastructure of the project.
2.2 Existing System
The implementation of smart technologies in the agricultural sector has proved to have a
substantial potential to solve the problems of productivity and sustainability in the global
agricultural sector. The integration of environmental sensors, wireless networks, cloud
platforms, and friendly interfaces is creating agricultural monitoring systems that allow
farmers to make informed decisions based on data about irrigation, fertilization, and pest
control practices. These systems are a significant change in the way farming is done, and they
have shifted the paradigm of farming that was previously based on the use of the traditional
methods to technology-based solutions that can make the best use of resources and increase
crop output.
2.2.1 Case Study 1: Smart Paddy Rice Production Framework
One of the most complex examples of smart agriculture application is the paddy rice
production framework created by Alfred et al. in 2021, combining the Big Data, Machine
Learning, and Internet of Things technologies to optimize the rice supply chain. This system
uses intelligent sensors that are installed in rice fields that record real-time environmental
conditions such as soil pH, soil moisture, temperature, and light intensity. The data collected
is analysed through sophisticated machine learning algorithms like Random Forest, Support
Vector Machine and Convolutional Neural Networks to fulfil various goals like predicting
15
yield, monitoring crop growth, detecting disease and managing irrigation. The system uses
hyperspectral imagery and UAVs deployment to provide remote sensing capabilities that
allow accurate estimation of rice productivity and detailed monitoring of crop health using
indicators such as chlorophyll content and leaf area index. Moreover, the smart irrigation
component made optimal use of water and did not reduce or even increase yields, whereas
ML-based image recognition made it possible to detect such diseases as rice blast earlier,
making the level of chemical treatment dependence much lower and the response time much
faster.
2.2.2 Case Study 2: IoT-Agro Coffee Farm System
Another solution to smart agriculture is the IoT-Agro system that Rodriguez et al. applied in
2021 to a coffee plantation in Colombia, which uses a complex three-layer system. The
system was to assist farmers in scheduling their harvests according to the climatic changes,
predict crop yields on an annual basis and prevent crop diseases by thorough analysis of
current and past data. The architecture is divided into a Perception Layer, which captures
environmental data with the help of IoT devices, including Omicron, Libelium, and Intel
sensor kits, an Edge Layer, which implements an outlier detection algorithm based on
Isolation Forest algorithms and provides data recovery, and a Data Analytics Layer, which
implements a machine learning-based coffee yield estimation algorithm, including the
XGBoost algorithm. The system also comes with a specialized web-based platform located
on www.iot-agro.com, which will give farmers access to sensor-based information, allow
planning of farming activities, and manage their infrastructure more efficiently and in a
timely manner.
2.2.3 Case Study 3: Smart Tomato Monitoring System
```
Siddiquee et al. (2022) came up with a smart tomato monitoring system in Bangladesh that
```
targets specifically the automated detection, quantification, ripeness assessment, and disease
identification in tomato fields. This system integrates IoT, computer vision, and machine
learning in an innovative mobile robot platform in the form of a camera that takes pictures in
the field and analyzes them with Circular Hough Transform, color segmentation, and CNN
algorithms. The CNN-based model demonstrated a remarkable 92% of detection accuracy
which is way higher compared to the traditional monitoring techniques in real-time crop
16
evaluation. The study, however, cited practical constraints such as bulky sensor apparatus and
high power consumption implying that in future, the research work should consider
integrating hybrid sources of energy that will make the monitoring system sustainable.
Although these three systems are similar in their purpose of allowing data-driven
decision-making toward better crop productivity and sustainability, they show substantial
differences in implementation scale, complexity of the technologies used, and resource
demands. The rice monitoring system described by Alfred et al. is a high-technology solution
that involves hyperspectral imaging and drone technology and is powerful and
comprehensive but has cost obstacles that could make it prohibitive to smallholder farmers in
developing areas. The coffee monitoring system proposed by Rodriguez et al. is more
modular, scalable and provides a three-layer architecture with more sophisticated computing
and web-based dashboards, yet still needs the reliance on comparatively costly sensor kits.
Comparatively, the tomato monitoring method of Siddiquee et al. is less complicated in terms
of methodology, and it is evident that camera-mounted robots and CNN models are much
more affordable, which proves that vision systems can be used to implement digital
agriculture.
17
2.3 Internet of Things
```
Internet of Things (IoT) is a revolutionary technology in contemporary precision farming that
```
offers new solutions to problems such as poor efficiency, low productivity, and sustainability.
The concept of IoT in agriculture may be referred to as a complex of interrelated physical
devices such as sensors, communication modules, and gateways aiming to gather, transmit
and process real-time data within farming ecosystems. This technology allows farmers to stop
relying on previous experience and manual observation and use real-time data collected in the
field with the help of sensors to carry out various processes, including irrigation, fertilizing,
```
and pest control (Amr et al., 2022).
```
IoT technologies make it easy to monitor key agricultural parameters such as soil moisture,
temperature, humidity, light levels, rainfall, wind velocity, and crop health parameters such as
soil moisture continuously. This information is sent via communication standards such as
Wi-Fi, ZigBee, LoRaWAN, or cellular networks to cloud services where it could be stored,
```
processed, and visualized in the form of mobile applications (Rajak et al., 2023). The
```
integration allows the farmers to control the information remotely, get notifications, and
receive immediate responses to irrigation, fertilization, pest control, and harvesting
```
requirements (Kumar et al., 2024).
```
2.3.1 Layered Architecture Framework
Figure 1: Layered Architecture of IoT Systems
18
The architecture framework of agricultural IoT systems includes four layers which are
Perception Layer, Network Layer, Middleware Layer, and Application Layer. The
hierarchical design allows the orderly transmission of data from physical agricultural settings
```
to practical actions to guide smart farming decisions (De Araujo Zanella et al., 2020; Morchid
```
```
et al., 2023). The Perception Layer is the base layer which has physical sensing devices
```
directly connected to the farming environment and they gather real time data based on
sensors like temperature, humidity, soil moisture, light sensors and automated response
actuators.
The Networking Layer serves as a gateway between the sensors deployed in the farm to cloud
services, and it supports short and long range wireless protocols based on field size and
weather conditions. Technologies such as Wi-Fi, Bluetooth LE, ZigBee, LoRa, NB-IoT,
SigFox, WiMAX, and 5G are communication technologies, and each of them has certain
```
benefits regarding the range, power consumption, and data rates (Tang et al., 2024). The
```
Middleware Layer is the stage where raw data from the sensors are processed, filtered and
interpreted to convey meaningful information to the Application Layer, which displays
processed information to end-users in the form of dashboards, mobile applications, alerts, and
```
decision support systems (Morchid et al., 2023).
```
2.3.2 Sensor Technologies and Selection Considerations
The performance of the IoT-based agricultural monitoring system greatly relies on the
selection of the sensors, where the selection is usually based on accuracy, cost, power
consumption, durability, and ease of integration. DHT22 sensors are ideal in terms of balance
between temperature and humidity sensing and power consumption with temperature
accuracy of ±0.5°C and relative humidity accuracy of ±2% at a low power consumption
```
(Santos & Santos, 2019). Soil moisture monitoring is enhanced by the use of Decagon EC-5
```
sensors, which are affordable with high accuracy and longer durability than cheaper options,
```
which are prone to corrosion (De Los Ángeles Calva Jiménez et al., 2019).
```
In pest detection applications, camera based surveillance is one of the major steps in
agricultural internet of things early warning systems, where harmful insects are automatically
detected using image processing and deep learning systems. In a list of considered solutions,
19
```
such as OV2640, Raspberry Pi Camera v2 (IMX219), and ESP32-CAM (OV3660), OV2640
```
appears to be the most appropriate solution to be applied in agricultural IoT. It provides a
```
great trade off in terms of cost, power consumption (60-80 mA active), and acceptable
```
```
accuracy (~90% with YOLOv5s/MobileNet) with lightweight deep learning models
```
```
(Subburaj et al., 2025). It supports ESP32, has JPEG compression abilities, and can be used
```
in battery/solar-powered installations, making it perfect in remote agricultural environments
```
(Subburaj et al., 2025).
```
The trade-offs are performance based, cost and power consumption, which is significant in a
resource-limited environment such as rural Malaysia. The less expensive sensors may be
applied in pilot studies and minor-sized surveillance of farms and the more accurate sensors
may be applied in large-scale agricultural activities that require comprehensive and
dependable data analysis.
2.3.3 Communication Technology Selection
LoRa technology is the most balanced communication technology in terms of smallholder
farms with ultra-low power usage, long-range transmission of up to 20 kilometers in rural
areas, and the use of unlicensed frequencies to enable the deployment of specific networks at
```
a low cost (Tang et al., 2024). Wi-Fi offers high data rates adequate to small-scale farms or
```
greenhouse environments but has a range limitation, power consumption, and infrastructure
dependence. In the meantime, NB-IoT uses licensed cellular networks with broader coverage
and good obstacle penetration, but it needs to have higher operation expenses and
accessibility of telecom services.
2.3.4 Platform Integration and Simulation
Selection of the hardware platform to integrate the sensors includes Arduino Uno, Raspberry
Pi, and ESP32. ESP32 comes out as the best option and it offers a good trade-off between
performance, power consumption, affordability, and built-in wireless communication features
built-in. It has a dual-core processor, including Wi-Fi/Bluetooth, and sleep mode, which
makes it suitable to collect and transmit sensor data in real-time in energy-limited rural
```
settings (OpenELAB, 2024).
```
20
Different simulation platforms such as Wokwi, Cisco Packet Tracer, and Proteus have
different capabilities in terms of development and testing. Wokwi is notable in agricultural
IoT development because of its accessibility via a web browser, real-time sensor emulation,
and support of prevalent agricultural sensors, which makes it especially suitable to rapid
prototyping and collaborative debugging without the need to install or run any software
2.3.5 Simulation Platforms for Real-Time IoT Environments
Simulation platforms are important in the development of agricultural IoT due to time
constraints, budget constraints, and access to hardware. On these platforms, developers are
able to create and test machine learning algorithms, evaluate the patterns of data flow, and
check the functionality of the system without physically deploying it. Artificial sensor
readings of temperature, humidity, soil moisture, and other parameters can be created through
simulation platforms through a realistic pattern such as temporal variation and random
variations that mirror the real farm conditions.
Three large cloud-based IoT simulation systems were considered: Ubidots STEM, IoTIFY
IoT Simulator, ThingsBoard Cloud. The platforms are all compatible with sensor data
simulation, cloud storage, visualization features, and data export to use in machine learning.
Ubidots STEM is the best solution to simulation of agricultural IoT because it has a friendly
interface, pre-loaded dashboard, cloud-based storage, and CSV export, and with free access
to education. Although IoTIFY provides more flexibility of using JSON scripting to define
complex sensor behaviors, it does not include storage and dashboard capabilities that need to
be integrated by other solutions. ThingsBoard Cloud offers a fully featured platform with
customizable dashboards and storage but restricts the use to 30 days free trial and is not
feasible in the long-term academic applications.
2.3.6 Regional Context and Adoption Barriers
Despite IoT's demonstrated potential to enhance agricultural productivity and sustainability,
```
implementation in Malaysian agriculture remains limited. Research by Mazlan Abbas (2023)
```
identified significant barriers including poor internet connectivity in rural regions, limited
technical knowledge among farmers, high costs of commercial sensor devices, lack of
awareness about available potential, and imperfect user-friendly interfaces. These challenges
21
indicate that successful IoT implementation in Malaysia requires solutions addressing local
infrastructure limitations, cost-effectiveness, and farmer-friendly design considerations,
particularly for smallholder farming communities.
2.3.7 Conclusion
AgriSense is an IoT monitoring system that has been carefully engineered to address the
current challenges of agricultural productivity and resource-efficiency in the Malaysian
agricultural sector. Although its practical application today uses simulation because of the
practical limitations of a project timeframe, budgeting limitations, problems of hardware
acquisition, and feasibility of the project, the overall technological analysis completed will
still make all the system components ready to be launched in the real world and properly
tested.
The specific choice of technologies, including the ESP32 microcontrollers and the LoRa
communication protocols themselves, as well as the particular sensor layouts, offers a full
blueprint of how this is to be implemented, thus ensuring a smooth shift to a physical
deployment at the first opportunity, once safe. Such a simulation-based method, employing
such platforms as Ubidots STEM, successfully maintains the integrity of the system, allowing
a comprehensive test of its agricultural monitoring algorithms, data processing processes, and
essential decision-making systems.
Finally, having developed AgriSense through a simulation-first implementation, the project is
an effective illustration of how, even when time and resources are constrained, advanced IoT
agricultural monitoring systems can still be developed and thoroughly tested without losing
the determination to physically deploy a solution. The strong technical basis described in this
review anchors the potential of AgriSense to be deployed successfully to solve practical
problems in the agricultural sector in Malaysia and other similar developing environments
when the deployment opportunity is presented.
22
2.4 Cloud Platform
The systematic integration of cloud computing in the agricultural IoT has been essentially
necessitated by the necessity to analyze large volumes of sensor data, to be cost-efficient and
scalable. The literature shows that cloud computing forms the foundation of collecting,
analyzing, and storing agricultural data, where field data is collected using cloud-connected
wireless sensors, which is then analyzed by machine learning algorithms in real-time to
```
present farmers with actionable information (Miller et al., 2025).
```
The shift between the on-premises and cloud-based agricultural systems has been widely
reported in numerous studies. Scientists always mention the ability of cloud platforms to
remove the physical hardware maintenance requirement and offer automatic scaling
```
opportunities and guarantee high availability due to managed infrastructure (Miller et al.,
```
```
2025). This transition has been especially useful to teaching and research initiatives and
```
small-scale agriculture enterprises that cannot afford large-scale IT infrastructure, leveling the
playing field in regards to access to advanced agricultural technologies.
2.4.1 Cloud Service Models in Agricultural Applications
Agricultural IoT applications are generally designed to take advantage of more than one
model of cloud services at once to maximize both utility and affordability. Infrastructure as a
```
Service (IaaS) offers the base computing infrastructure that is required in the storage and
```
```
processing of the data. Platform as a Service (PaaS) provides development frameworks that
```
are specifically designed for the agricultural application and, thus, allow the rapid prototyping
```
and deployment. Software as a Service (SaaS) provides farm management tools that are ready
```
```
to use and implement by farmers without any technical knowledge (Miller & Shekhar, 2024).
```
23
2.4.2 Major Cloud Platform Implementations in Agriculture
Figure 2: Collaboration between Big Tech companies and Cloud Platform
```
2.4.2.1 Amazon Web Services (AWS)
```
AWS has built a strong market presence in the IoT of agriculture due to the depth of service it
offers and industry partnerships. A good example of successfully implemented AWS is the
BASF Digital Farming that utilizes the National Oceanic and Atmospheric Administration
```
(NOAA) weather data available on AWS as well as commercial weather data to create digital
```
```
solutions that enable farmers to monitor and manage their fields efficiently (Goodman,
```
```
Simonson, Oyler, & Dissen, 2021). This combination of commercial and government data
```
sources shows that AWS can handle complex agricultural analytics that need multiple data
sources, which is essential to complete agricultural decision-support systems.
24
The mature platform of AWS with a lot of documentation and learning resources makes it
especially fit to be used in academic projects that need a lot of development resources.
```
Amazon Relational Database Service (RDS) on the platform offers programming to automate
```
backup, software patches, and monitoring that is particularly applicable to agricultural
```
monitoring demonstrations (Bhalekar, 2024). However, the pricing system of AWS can be
```
complicated, which can cause unforeseen expenses outside the free level, especially
regarding the time of development in academia. Such pricing complexity is a major challenge
```
to educational implementations where predictability of budget is paramount (Bhalekar, 2024).
```
2.4.2.2 Microsoft Azure
```
The new development in the Controlled Environment Agriculture (CEA) has been more
```
dependent on cloud computing to improve the management of data, automation, and
```
scalability of systems. The IoT-based system architecture suggested by Srimal et al. (2024)
```
involves the Microsoft Azure services, namely, Azure IoT Hub, Azure Stream Analytics, and
Azure SQL to design a real-time data-driven smart agriculture environment. Such tools allow
a high degree of monitoring and control of environmental variables, which facilitate optimal
growth conditions and higher yield in high-tech greenhouse systems. The combination of the
cloud-native services of Azure enables the connection of sensors and actuators in an
uninterrupted manner, providing real-time feedback and predictive opportunity of precision
farming. Additionally, the architecture takes advantage of the scalable infrastructure and
economic resource provisioning of Azure that are essential to sustainable and
```
high-throughput agricultural processes (Srimal et al., 2024).
```
Besides the technical scalability, Azure has several economic and developmental benefits that
render it especially useful in agricultural innovations. Among the primary advantages are the
cost-efficient pricing systems of Azure, such as its consumption-based billing, which enables
```
the agricultural projects to grow without having to spend money on the infrastructure (Daniel
```
```
et al., 2024). This can be particularly helpful to research organizations and start-ups in the
```
agriculture-technology sector where limited funds are a concern. In addition, Azure offers
free-tier services and educational credits to universities and academic programs, which
dramatically decreases the financial threshold to the student-led or prototype-phase
```
agricultural IoT implementations (Ojika et al., 2023). Developer productivity is also
```
25
optimized by the high level of integration of Azure with popular development tools like
Visual Studio Code, GitHub and Python libraries, allowing quicker deployment and iteration
cycles. The combination of these abilities makes Azure more than just a strong cloud
backbone to precision farming, but also a platform that enables cost sustainability, speed of
innovation, and inclusive access in the digital transformation of agriculture.
```
2.4.2.3 Google Cloud Platform (GCP)
```
```
Thilakarathne et al. (2022) introduce a cloud-based crop recommendation system capable of
```
```
utilizing the Google Cloud Platform (GCP) to create an AI-based precision farming
```
application in their study. The system uses machine learning algorithms combined with farm
data such as soil, weather and crop characteristics to suggest the best crops for real-time
conditions. Platform deployment was done by using GCP services like Google App Engine
and allowed high availability and easy scalability. The method saves farmers and researchers
on computational overhead as it provides a more efficient data-driven decision-making
process in sustainable agriculture. The article reveals the need to incorporate smart
recommendation engines into the farming ecosystems to achieve productivity and reduce
wastage of resources.
Scalability and low-cost flexibility of Google Cloud are also positive features of the academic
and small-scale agricultural uses by the authors. With the help of the GCP
```
Platform-as-a-Service (PaaS) model, it avoids the difficulties associated with infrastructure
```
```
management and preserve the strong backend functionality (real-time access to data,
```
```
cloud-based and API-based interaction, and automatic retraining of the models). Also,
```
Google Cloud and its scalable computing environment will enable the project to scale
```
eventually into very large datasets and sensor-based Internet of Things (IoT) systems. This
```
paper shows that it is possible to deploy cloud services to support intelligent agriculture
```
platforms and presents a straightforward framework of how to use GCP (and maybe similar
```
```
web-based cloud-computing utility model toolkits) to enable academic and research-based
```
precision agriculture systems.
2.4.3 Cloud Platform Selection
26
Criteria AWS Azure GCP
Database PostgreSQL,
MySQL, SQL Server
PostgreSQL,
MySQL, SQL Server
PostgreSQL, MySQL,
SQL Server
IoT Integration AWS IoT Core Azure IoT Hub Google Cloud IoT
Cost-Friendliness Good for short-term,
expensive long-term
Most cost-friendly Good with sustained
use discounts
Free Tier 750 hours/month,
20GB storage
750 hours/month,
32GB storage
$300 credits +
always-free
Scalability Excellent
auto-scaling,
complex pricing
Superior elastic
scaling options
Exceptional
auto-scaling
Ease of Use Difficult Moderate Moderate
Table 1: Cloud Platform Comparison Table
Microsoft Azure is chosen as the cloud platform of this agricultural IoT early warning system
based on the comparative analysis. The reasons to choose this selection are educational
advantages such as generous educational credits and long free usage period, predictable costs
with clear pricing mechanisms, and high compatibility with common development tools in
academia. The high cost-efficiency and average usability of Azure are what make it most
suitable for academic applications aimed at the demonstration of agricultural monitoring
concepts.
2.4.4 Conclusion
The overall analysis of cloud platforms in agricultural IoT early warning systems reveals that
Microsoft Azure will provide the most suitable background to academic applications because
it is affordable, educative, and technically-sufficient. The agricultural data processing has
changed due to the transition of on-premises systems to cloud-based, as infrastructure
obstacles are eliminated, and real-time monitoring and decision-making are possible. Azure
can be distinguished among AWS and GCP due to its educational benefits, predictable prices,
built-in IoT capabilities, such as Azure IoT Hub, and the ability to support academic
development environments, which makes it a good choice to teach about agricultural
monitoring, yet has the potential to be upgraded at scale in the future.
27
2.5 Database
The development of database technologies in agricultural IoT early warning systems is
associated with the high necessity of real-time data processing and ensuring the integrity of
the alert generation. Modern IoT-based weather and pest risk management early warning
systems require the processing of constant environmental monitoring data and fast
decision-making cycles that pose special database needs that are distinct to other agricultural
information systems.
Weather and pest management early warning systems need databases that can operate high
frequency sensor data in low latency response times to critical alerts. These two needs have
led to the implementation of specialized database architecture better suited to time-sensitive
agricultural tasks, which has fundamentally altered the structure, storage, and access of
weather and pest surveillance information in support of decisions.
2.5.1 Single Database Architecture
Single-database architecture has become a practical and effective design of agricultural IoT
systems, especially in academic and proof-of-concept systems. This architecture uses a single
unified relational database, e.g. PostgreSQL, to handle all of the main data types, including
sensor telemetry, user management, etc., within a single schema. This abstraction makes
development faster, less complex in integration and easier to maintain. Pereira, Rodrigues,
```
and Trilles (2024) demonstrated that PostgreSQL, with the proper configuration of table
```
design and the use of time-based indexing schemes, may handle bulky volumes of agri-sensor
data effectively. In even high-ingestion applications, such as weather or soil monitoring, a
single PostgreSQL instance could keep the data intact, enable consistent access control, and
minimize the overhead of operating multiple data sources. Additional performance
enhancement using optional extensions such as TimescaleDB did not change the relational
organization of PostgreSQL, making it a suitable choice of end-to-end IoT data management.
2.5.2 Relational Database Technologies in Agricultural Applications
2.5.2.1 PostgreSQL
28
PostgreSQL, especially when combined with PostGIS has been very useful in geospatial and
temporal data applications in the agricultural sector. Its features render it appropriate in
monitoring and assessing environmental factors like precipitation, soil moisture and pest
```
movement. Hess (2022) has shown how PostgreSQL and PostGIS can be used to create a
```
spatial database of regenerative farming, which allows managing spatial data and archiving
efficiently. Its powerful indexing, good transaction management, and the open-source
adaptability of the database makes it suitable to use in early warning and geospatial
surveillance in smart agriculture.
```
This can be further illustrated in the work of Kamati, Hashiyana, and Mutuku (2024), who
```
have built an almost real time agricultural disaster prediction system with the use of
PostgreSQL with PostGIS in order to manage and query the georeferenced crop, weather and
sensor data. Their system also facilitated effective spatial analytics such as pest prone areas
and flood prone areas, even though the data integrity and scalability was maintained. The
paper attests to the usefulness of PostgreSQL as a centralized spatial-relational backend in
early warning systems, which is able to provide both operational resilience and analytical
richness in the context of smart farming applications.
2.5.2.2 MySQL
The MySQL has demonstrated to be a feasible and efficient solution to the IoT-based
agricultural systems in Malaysia, especially in academic and experimentation where
simplicity, cost-effectiveness, and low processing overhead are paramount. It is perfectly
compatible with microcontroller systems like Raspberry Pi and Arduino, which makes it
suitable to collect and store data in real-time in resource-limited conditions. In one
```
experiment, Ramli et al. (2023) designed a smart portable farming kit to use in growing crops
```
indoors by using Raspberry Pi to measure the temperature, humidity, and light intensity of the
environment. MySQL was installed as the local database in order to store and retrieve sensor
data, allowing the responsive monitoring by a locally hosted interface. This arrangement
emphasized the use of MySQL in providing fast data access without the need to use cloud
infrastructure, which made it more appropriate in rural and small-scale farming initiatives.
```
Similarly implemented, Zaki et al. (2025) designed a smart monitoring system for durian tree
```
farming that combined soil moisture and temperature sensors and a Raspberry Pi controller.
29
To transfer sensor data, MQTT was used, and all the data was stored in a MySQL database,
which allowed farmers to check and control the status of irrigation in real-time via an
intuitive web interface. This design proved that MySQL was capable of lightweight,
distributed systems which can fit the limitations of smallholder agriculture. The two studies
confirm the success of MySQL in facilitating effective data management and quick
decision-making in the emerging IoT agriculture sector in Malaysia.
2.5.2.3 SQL Server
Microsoft SQL Server is a powerful enterprise-level relational database management system
which has been applied in smart agriculture environments where structured data needs to be
stored, traceable and securely analysed. Its cloud ecosystem and business intelligence tool
like Power BI integration makes it very suitable for complex agricultural operations that
```
require long-term monitoring and decision support. As an example, Aydin and Aydin (2020)
```
developed a multi-layer data processing model in hazelnut production and applied Microsoft
SQL Server as a central database to collect and handle semantically enriched sensor data. The
system monitors the soil and environmental parameters in real-time and to facilitate
automated decision-making processes via the web-based interfaces. This case points to the
ability of SQL Server to serve in agriculture-focused IoTs which require high levels of data
integrity and compatibility with sophisticated analytical tools.
Nevertheless, regardless of these advantages, it can be observed that there are not many
documented applications of Microsoft SQL Server in agriculture-specific IoT systems. The
majority of the existing systems prefer open-source alternatives like MySQL or PostgreSQL
because of cost, community support, and simpler integration with microcontroller-based
environments. This gap opens up a potential research or implementation of SQL Server
supported smart farming systems, particularly in government or enterprise-sponsored projects
that may need more security, compliance, and data governance.
2.5.3 Relational Database Selection
Criteria PostgreSQL MySQL SQL Server
Cost-Friendliness Free Free Free for Express
30
Scalability Excellent Good Excellent
```
JSON Support Excellent (JSONB) Good Good
```
Ease of Use Moderate Easy Moderate
```
Spatial Data PostGIS Limited (Plugin) Supports but
```
proprietary
Educational
Resource
Excellent Excellent Good
Table 2: Relational Database Management System Comparison Table
According to the comparative study and needs of this agricultural IoT early warning system,
PostgreSQL has been chosen as the main database system. This choice is explained by its
outstanding JSONB support of the IoT sensor data, high scalability, low price as an
open-source product, and vast number of educational materials that can be used in academic
implementations. The PostGIS extension of PostgreSQL also provides useful spatial data
features to be used in the future.
2.5.4 Conclusion
The detailed review of database technologies of agricultural IoT early warning systems shows
that PostgreSQL offers the best platform to be used in academic applications. The decision to
select the unified relational database instead of the complex hybrid architecture is based on
the practical requirements of this academic project that give priority to the efficiency,
cost-effectiveness, and maintainability of the development rather than the theoretical
performance optimizations. The choice of PostgreSQL can be explained by its excellent
JSONB support of flexible IoT data models, strong scalability properties, the low cost of an
open-source solution, and rich educational materials, whereas the PostGIS extension provides
welcome spatial data features that can be applied to the future extensions of the work, so this
database is especially appropriate in the academic agricultural IoT projects aimed at proving
the real-time monitoring and alerting possibilities.
31
2.6 Machine Learning
This literature review will discuss the machine learning methods to predict weather
conditions and detect pests in agricultural systems with the emphasis on models that can be
deployed in mobile systems. The analysis compares the different algorithms with respect to
accuracy, computational efficiency and their practical applicability to the agricultural decision
support systems with special focus on implementation in resource-limited systems.
2.6.1 Weather Prediction Model
2.6.1.1 Regression-Based Approaches
```
A study conducted by Biswas et al. (2024) showed that Long Short-Term Memory (LSTM)
```
networks performed better in temperature forecasting with a remarkably low Mean Absolute
```
Error (MAE) of 0.002 and Root Mean Square Error (RMSE) of 0.045 when evaluating the
```
model on a huge Delhi weather dataset of 96,456 data points. XGBoost performed
```
moderately (MAE: 0.149, RMSE: 13.91), whereas K-Nearest Neighbors had an accuracy of
```
about 75%. The paper has cited the high performance of LSTM to the fact that it is effective
in modeling sequential dependencies in the weather data.
```
Subramanian et al. (2025) performed climate modeling in Malaysia with Support Vector
```
```
Regression (SVR), Random Forest Regression (RFR), and Linear Regression (LR) based on
```
the historical data of the year 2014-2024. Linear Regression performed the best among all
methods in predicting temperature with MAE of 0.0894 which is significantly better than
```
SVR (MAE: 0.2442) and RFR (MAE: 0.3514). Nevertheless, every model was not good at
```
```
predicting precipitation, and SVR still had a rather low performance (MAE: 4.9603), showing
```
that rainfall is a complex phenomenon in the tropics.
2.6.1.2 Classification-Based Approaches
```
Chong et al. (2025) created a weather forecasting system on the web, which was based on
```
```
Random Forest, K-Nearest Neighbors, and Multilayer Perceptron (MLP) models that were
```
trained on 22 years of real-time weather data. In case of hourly forecasting, MLP recorded
```
the best accuracy of 97.61%, followed by KNN (86.19%) and RF (84.86%). Nevertheless,
```
32
MLP was prone to overfitting and consumed too much computing resources. It was
concluded that Random Forest was the most appropriate to deploy in practice, because of its
stability and computational efficiency.
```
Premachandra and Kumara (2021) suggested a binary classification model of the rainfall
```
prediction system in Sri Lankan agriculture. The best accuracy of 89.16% was obtained from
Random Forest, and the second-best was KNN with 88.66%, and SVM with 88.57%,
indicating the effectiveness of algorithms that are tailored to specific tasks, such as
classification. Multiple Linear Regression that is adapted to classification tasks performed
very poorly at 44% accuracy. When testing the four machine learning algorithms on the
```
weather data of Seattle, Oshodi (2022) found that the Gaussian Naive Bayes had the highest
```
```
accuracy of 84.15%, compared to the Gradient Boosting Classifier (80.87%) and Random
```
```
Forest (79.50%), proving that simpler algorithms can also perform better than complex
```
ensemble models in situations where the available dataset is limited.
2.6.1.3 Model Selection Rationale
According to the thorough analysis, three models were identified to be used in agriculture.
Random Forest was the first recommended because it was performing consistently in most
studies with an accuracy of 79.50% to 89.16%, and it showed a high level of stability in
various parameter configurations and computational efficiency that is compatible with mobile
implementation. This capacity of the model to rank the features in terms of their importance
is especially useful when interpreting the meteorological factors influencing the agricultural
decisions.
The second candidate, XGBoost, was chosen due to its demonstrated performance on large
data and its ability to handle complex non-linear relationships which are often characteristic
of weather data, although its regularization properties are in-built, which helps prevent
overfitting, and thus it will work well in the unpredictable tropics climate pattern of Malaysia.
The third option was the Multi-Layer Perceptron which is likely to have the highest accuracy
as it has recorded 97.61% accuracy in the optimal settings, better ability to recognize
non-linear patterns and is also suitable in capturing seasonal and regional climatic variations
that are characteristic of the tropical climate.
33
2.6.2 Pest Computer Vision
2.6.2.1 Traditional vs Deep Learning Approaches
```
Kasinathan et al. (2021) carried out a broad comparison between traditional machine learning
```
and deep learning methods of insect classification on various datasets in their study.
Traditional approaches using shape based feature extraction did not perform that bad, with
```
Support Vector Machines using radial basis function kernel extracting 79.9% (9 classes) and
```
```
75.8% (24 classes) accuracy. However, Convolutional Neural Networks far surpassed the
```
conventional methods by achieving the accuracy of 91.5 and 90% respectively on the same
sets of classes. The study demonstrated that deep learning models can automatically learn
features in a superior manner than when using manual feature extraction methods but that
they require increased computational resources.
2.6.2.2 Real-Time Detection Systems
```
The study by Onler et al. (2021) created a real-time system to detect pests with YOLOv5
```
architecture to detect thistle caterpillars that negatively impact sunflower cultivation. Out of
four versions of YOLOv5 tested, the best mAP of 59.1% was obtained using transfer learning
in YOLOv5m and the fastest speed of detection with 65 FPS was obtained in YOLOv5s, the
latency of which was minimal 15.3ms. This study demonstrated the significance of transfer
learning because models trained randomly performed poorly relative to pre-trained models.
```
The authors of the study by Yang et al. (2023) developed Maize-YOLO, an improved version
```
of the YOLOv7 model that is more suitable to detect maize pests. The model used custom
modules CSPResNeXt-50 and VoVGSCSP with mAP of 76.3% and recall of 77.3%, and the
speed of detecting in real-time of 67 FPS. Maize-YOLO performed better than standard
models, such as YOLOv3, YOLOv5, RetinaNet, and Faster R-CNN in mAP with less
computational resources, proving the viability of highly-specific agricultural pest detection.
```
Maican et al. (2023) trained a lightweight model of pest detection created with the
```
MobileNet-SSD optimized to run on the mobile device with a low power consumption.
MobileNet-SSD-v2-Lite obtained 0.892 in mean mAP and good class-specific mAP with
95.14% and 80.66% of Opatrum and Diabrotica, respectively, using a two-step transfer
34
learning. Notably, the model had a zero false positive rate on the beneficial insects, such as
Coccinella, which indicates that it can work to differentiate between the harmful pests and the
beneficial ones.
2.6.2.3 Model Selection Rationale
Three models were identified based on thorough assessment to be deployed in the agricultural
field. The main candidate was chosen to be YOLOv5s, because of its good generalization
ability, reaching 57.5 mAP with transfer learning, and the fastest inference speed of 65 FPS,
which makes it suitable to use in real-time mobile detection. The model is widely supported
by the community and documented, which makes the model reliable during implementation.
The second option was YOLOv7-tiny, which provides a great trade-off between accuracy
```
(67.7% mAP) and efficiency (204 FPS) and has a relatively small number of parameters (6.1
```
```
million), so it can be used on resource-limited devices. Its high performance feature
```
extraction ability and fast training time enables fast model development and fast iteration in
agricultural application.
The third option MobileNet-SSD-v2-Lite was selected because it is specifically optimized to
work with mobile devices and has demonstrated high performance in separating harmful
pests and beneficial insects. Its mAP of 0.892 speaks of its potential to be deployed on
smartphones and IoT devices as commonly used by farmers in places with low connectivity
and computing resources.
2.6.3 Conclusion
This literature review shows that there has been a major development in the area of machine
learning in predicting the weather in agriculture and detecting pests. Random Forest,
```
XGBoost and Multi-Layer Perceptron (MLP) were chosen to predict weather, with
```
reasonable stability, efficiency and potential high accuracy. Deep learning models were found
to be the best in pest detection, and YOLOv5s, YOLOv7-tiny and MobileNet-SSD-v2-Lite
were selected as the best combination of accuracy, speed, and mobile deployment. These
choices are the foundations of AgriSense, an integrated mobile early warning system of
precision agriculture.
35
2.7 Mobile Application
2.7.1 User Interface Design
The design of the user interface is a very important aspect that will ensure that mobile
agricultural applications are easily usable and adopted, especially by smallholder farmers in
rural settings who will be having their first exposure to digital agricultural tools. The
interface has to be able to make complex agricultural information more easily accessible and
present it through an intuitive, user-friendly interface that is accessible to those with different
levels of digital literacy and technical skills.
2.7.1.1 Design Challenges in Agricultural Contexts
The development of user interfaces in agricultural applications is associated with peculiarities
that are not typical of the development of ordinary mobile applications. The target users
include many people with little experience with smartphones, with different literacy levels,
and use their smartphones in unfavorable environmental conditions such as sunlight, dust,
and unreliable internet connections. Such practical limitations have a great effect on interface
```
perception and usability (Ibrahim & Danmaigoro, 2024). Also, such highly technical,
```
word-heavy, or cluttered interfaces may intimidate users and deter use, especially in
low-resource rural environments.
2.7.1.2 Essential Design Principles and Best Practices
Icon-Based Navigation and Minimal Text Usage
A good agricultural UI design focuses more on visuals and icons rather than large bodies of
text. Icons must be easy, culturally acceptable and relevant to the intended population
```
(Osman etal., 2022). This is especially advantageous to the users with low literacy skills who
```
might not be able to navigate through the text-rich navigation screens and, at the same time, it
also lightens the cognitive load on the rural users.
Large Touch Targets and Simplified Layouts
```
Elements of the interface (buttons, icons, etc.) should be large enough to be easily operated in
```
outdoor conditions. In accordance with the principles of the Fitts Law, the bigger the button,
36
```
the less time and effort is needed to select it properly (Setiyawati et al., 2022). The menu
```
structures ought to have shallow hierarchies that are easy to understand, with no more than
3-5 top-level items, adhering to Hick's Law to reduce time and confusion by the user.
Audio Support and Interactive Voice Response Integration
Audio interfaces have good accessibility options to users who have low levels of reading
```
proficiencies. Audio feedback and Interactive Voice Response (IVR) can take the user
```
through applications without reading or typing skills. IVR systems have already been applied
into several successful agricultural projects to provide instructions and advice to smallholder
```
farmers (Osman et al., 2022).
```
Color Indicators and Visual Alert Systems
Colored features give instant feedback about essential agricultural data. Color use as strategic
```
tool (green signals to indicate good conditions and red warnings to indicate pests or unusual
```
```
soil conditions) allows the user to make informed decisions in a short period of time without
```
```
reading detailed explanations (Setiyawati et al., 2022).
```
Data Visualization Techniques
Good data visualization such as line graphs, trend charts, and heat maps enable farmers to
monitor the changes in environmental variables over a period. The visualizations that are well
designed facilitate the decision making process in the field of agriculture by ensuring that the
complex data is easily comprehensible and farmers have expressed preference towards
```
visualization in the form of graphs rather than raw numerical data (Setiyawati et al., 2022).
```
2.7.1.3 Analysis of Existing Agricultural Applications
IoT-Integrated Hydroponic Monitoring Application
This is a student-made system that has a well-organized dashboard that tracks major
```
parameters such as temperature, humidity, pH, and Total Dissolved Solids (TDS). The
```
interface presents the information in well-marked cards with big fonts and high-contrast color
that is appropriate to outdoor use. Navigation uses a bottom navigation bar with simple icons,
but the system doesn’t use the emphasis of warning alerts or real time visual prioritization
```
(Chan, 2024).
```
37
```
Figure 3: Monitor Panel Screen (Chan, 2024)
```
Agrio - Professional Plant Diagnosis Application
Agrio is a business product that provides pest and disease warning, image-based diagnosis,
treatment recommendations, and weather information. This design focuses on real-time alerts
using red banners, alert icons, and pop up cards with short and contextual messages. The
application is successful in terms of a visual and text balance, and it is not inefficient in
```
decision-making and fast interpretation of information (Agrio, n.d.).
```
```
Figure 4: Agrio User Interface (Agrio, n.d.)
```
38
Key Design Insights
Some of the key insights of the analysis include, visual prioritization with color-coded alerts
is more effective than technical listing strategies, simplified navigation with bottom
navigation bars is user friendly and promotes accessibility, dynamic alert-based content and
action-oriented prompts assist in user engagement, and the use of warning colors and familiar
icons to promote user experience among low literacy users.
2.7.2 User Experience
User experience includes the total perception, emotions, and response users give when using
agricultural mobile applications. UX plays an important role in rural farming settings to
guarantee user satisfaction, long-term involvement, and effective adoption of technology
among users who might not be exposed to digital tools. Good UX design helps to reduce the
distance between the sophisticated data on agriculture and the decision-making requirements
```
of farmers with visible, effective and emotionally satisfying interactions (Osman et al., 2022;
```
```
Setiyawati et al., 2022).
```
2.7.2.1 Key UX Factors
There are a number of aspects that lead to a good user experience in agricultural applications.
Simple learning makes the application simple to use without necessarily involving much
training. Efficiency helps the user to execute the most important functions that include
reading weather data or examining soil conditions with a minimum number of actions and
time losses. User satisfaction is associated with the enjoyment and ease of use of the
application, and it is directly connected with the visual design as well as responsiveness of
the application. The aspect of accessibility considers different levels of literacy and
smartphone use by offering different ways of input e.g. by audio or using icons. Lastly,
system feedbacks are immediate and explicit to confirm effective inputs, or warn the users of
problems.
2.7.2.2 UX Design Implications for Agricultural Applications
To design user experience in agricultural apps, it is necessary to make sure that interfaces are
clear and responsive. It must be easy to navigate with as few clicks as possible to be able to
39
access most important features such as weather alerts or land condition monitoring. There
should be instant visual feedback to assist users to know about the system or verify actions
performed. The app must give the user a sense of control and understanding, particularly of
those with lesser experience, and focus on ease, quickness and emotional reassurance.
2.7.3 Mobile Frontend Development Framework Selection
Cross platform development strategies enable developers to develop applications that can be
used on both Android and iOS platforms with the same codebase and save developers time
and effort in developing applications and ensure consistency in user experience across
systems. Framework selection is one of the most important decisions in mobile application
development because it determines the nature of the application itself.
2.7.3.1 Cross-Platform Framework Comparison
Flutter
Google created Flutter, based on the Dart programming language, enabling developers to
develop natively compiled applications that can be used in mobile, web, and desktop
applications using a single codebase. Flutter provides expressive and flexible UI possibilities
by providing rich pre-designed widgets and total control of screen rendering. Practical
```
applications developed by Leng (2023) shows that Flutter can manage complicated UI, live
```
data, and geolocation services.
React Native
Meta React Native is a framework based on JavaScript or TypeScript that compiles mobile
applications into native components linked to native UI components. The system is well-liked
because of the short development cycles and availability of rich library ecosystems. Chan
```
(2024) implemented a hydroponic monitoring system to demonstrate React Native is strong
```
in terms of real-time data processing and integration with different third-party services.
40
2.7.3.2 Programming Language Considerations
Dart
Dart is a strongly typed, object-oriented programming language, which is both ahead-of-time
```
(AOT) and just-in-time (JIT) compiled, which helps make Flutter fast and have a responsive
```
UI. The language has a clean syntax that is known to programmers with Java or C-like
language experience, but has a smaller community than JavaScript.
JavaScript
JavaScript is a broadly used scripting language utilized in web, server and mobile
applications, which is dynamically typed. JavaScript is used to run interface logic and interact
with native modules in React Native settings. It is dynamically typed, which permits a fast
development, but it can also present runtime errors and complexity in debugging of large
applications.
2.7.3.3 Framework Selection Rationale
Both Flutter and React Native have well-developed cross-platform mobile development
features. React Native is best used in quick prototyping and integration of the JavaScript
based ecosystem and is better suited in simpler or web-based applications. Flutter is unique in
its ability to perform better in terms of UI, organized development paradigms, and smooth
cross-device rendering. In the case of agriculture where the responsive interface and real-time
alert notification are needed, Flutter and Dart offer performance and tooling advantages that
```
enable long-term scalability and user experience needs (Sharjeel Moqrab Khan et al., 2022).
```
2.7.4 Conclusion
The review of the literature shows that the key to the successful use of agricultural mobile
applications is the thorough approach to the user interface, user experience, and the selection
of an adequate technology stack. To ensure that the farmers with different digital literacy
levels and severe environmental conditions can use it, UI design should be simple, accessible,
and visually clear. The most important design principles are the use of icons to navigate, large
touch targets, audio, color-coded messages, and proper data visualization.
41
The user experience design must revolve around the ease of learning, efficiency, satisfaction,
accessibility, and immediate feedback so that the rural users can adapt to the technology and
use it in the long term. The review of the current agricultural applications proves that visual
prioritization, simplified navigation, and dynamic alert systems are significant in the
development of effective user interfaces.
In terms of technology choice, Flutter with Dart stands out as an optimal choice of
agricultural application, as it is faster, has a consistent UI framework, and fits well with
responsive and alert-based interface design. Although React Native is more effective in rapid
prototyping and integration with the JavaScript ecosystem, Flutter has the performance
characteristics required in complex agricultural applications in adverse environments due to
its compiled nature and a custom rendering engine.
42
2.8 System Backend
The role of backend systems in the agricultural IoT acts as the central orchestration hubs that
coordinate the flow of data between sensors, machine learning models and user interfaces to
provide reliable and robust operation in a variety of operational conditions. IoT backends
have their own challenges such as the heterogeneous data formats, the fact that the collection
frequencies differ, and the fact that there is a need to support small farms and large-scale
operations. The backend serves as a data aggregation point and a computational engine,
where data about agriculture is analyzed using machine learning algorithms to produce
actionable insights in the form of mobile applications, making a smooth transition between
```
the data collection and decision-making processes (Symeonaki et al., 2020; Cravero et al.,
```
```
2022).
```
The evolution of backend architectures in agricultural systems has paralleled broader
software architecture trends, moving from simple monolithic applications to complex
distributed systems designed to handle modern agricultural requirements. Early agricultural
information systems relied on centralized architectures suited for batch processing and
periodic data collection. However, with the growing integration of real-time sensors and
mobile applications, modern backend infrastructures must now support continuous data
streams, multi-user concurrency, and complex analytics, all while maintaining responsiveness
```
and scalability (Trilles et al., 2020; Rathore et al., 2024).
```
2.8.1 Architectural Pattern Analysis
The monolithic architecture has its strengths and weaknesses when it comes to the use of
```
agricultural IoT. Aydin and Aydin (2020) explain, it bundles all the application components
```
into a single deployable package, which is effective in development simplicity, debugging
simplicity, and deployment simplicity, especially when it is used in a small-scale or academic
environment. Monolithic systems also support data consistency and ease of transaction
between modules due to their centralized system, which makes it effective in an environment
```
with limited development resources (Trilles et al., 2020). As an example, in prototype-based
```
projects such as AgriSense monolithic designs provide quick prototyping and logical control
over interdependent parts.
43
But as the system becomes more complex, the monolithic systems become severely
challenged by scalability. To give an example, updates usually necessitate the redeployment
of the whole application, and technology options are restricted to the single stack, leaving no
possibility to integrate heterogeneous systems like machine learning with Python and
```
processing in the real-time with Node.js (Olabanji, 2022). The problem is particularly
```
restrictive in contemporary farming where various modular technologies are frequently
required.
To overcome these difficulties, microservices architectures provide a more flexible
application since it involves the decomposition of backends into separate services that
```
communicate through APIs (Abgaz et al., 2023). This enables the scaling of only the needed
```
modules, e.g. data processing during peak seasons, and leaving the user-facing components
stable. Also, it allows the diversity of technology, such as Python for machine learning units
and Node.js or GO handling streaming data, as demonstrated in cloud-native agricultural
```
systems (Kamisetty et al., 2023). Nevertheless, this flexibility is a trade-off. The inter-service
```
communication also causes network latency, and distributed microservices can be far more
```
difficult to debug as compared to monolithic systems (Kamisetty et al., 2023).
```
```
Figure 5: Layered Architecture (Dauda et al., 2024)
```
44
Thus, one of the possible alternatives is a layered architecture. Dauda, Flauzac, and Nolot
```
(2024) note that layered systems divide functionality into application layer, service support
```
and application support layer, network layer and device layer, which makes development
simple and allows maintainability and separation of concerns and is especially effective when
used in educational contexts. Layered architecture can therefore be used to enhance
educational implementation aims and still maintain the advantages of scalability and
testability.
2.8.2 Backend Technology Selection
2.8.2.1 Python with Flask
The popularity of Python in agricultural backend development can be attributed to its
exclusive combination of web development and machine learning. According to Bhatt et al.
```
(2024), Python’s large adoption in smart agriculture is mainly due to the availability of
```
libraries like NumPy, Pandas and scikit-learn, which simplify the transition between data
collection, processing and predictive analytics. These functions facilitate integrated
development environments of agricultural systems that need both control interface and
analysis capabilities. The choice of framework has a factor such as Django offers all-in-one
capabilities with ORM and administration panels, to allow quick prototyping, whereas Flask
```
is more flexible and allows lightweight and customizable deployments (Chan, 2024).
```
2.8.2.2 JavaScript with Node.js
Node.js is especially applicable in real-time agricultural monitoring. It has an event-driven,
non-blocking I/O architecture that can handle a large number of concurrent connections to
sensors and field devices, enabling the scalable deployment of real-time dashboards and
```
control systems (Koumandrakis, 2022). APIs are also easier to create with frameworks such
```
as Express.js and can be integrated with WebSocket or MQTT, which makes Node.js a good
```
choice of responsive agriculture applications. Nevertheless, as Bhatt et al. (2024) note as
```
well, Node.js is not as effective in incorporating machine learning capabilities. It is not as
ideal as Python in terms of ecosystem development, which is why it would not be as suitable
to systems such as AgriSense that need to have unified analytics and service delivery on a
single stack.
45
2.8.2.3 Java with Spring Boot
Java Spring Boot is suitable for enterprise-scale agricultural systems because of its
performance, modularity, and strong integration opportunities. According to Tomar, Aeron,
```
and Ahmad (2024), Spring Boot allows layered architecture and secure and scalable services
```
that are essential to complex agricultural platforms. Additionally, Kumar, Goyal, and Gandhi
```
(2021) note that it is compatible with such technologies as blockchain and APIs, which
```
makes it suitable when high reliability is required. The complexity and dense configuration of
the framework may however slow down rapid prototyping and thus is not very useful in
academic or small-scale projects where simplicity and experimentation are important.
2.8.2.2 Backend Technology Selection Rationale
Frameworks written in Python have become a viable option when it comes to backend
development of agricultural IoT systems, especially when web services are integrated with
```
data management. Ghimire (2020) notes that Flask and Django are both well-supported in
```
academic development environments, where Django is an all-in-one framework that is suited
to building structured applications, and Flask is more flexible and suited to building
lightweight and modular projects. This trade-off between usability and minimalism renders
Python frameworks extremely appropriate towards educational and research-driven
agricultural systems, where quick development and cross-disciplinary cooperation are
critical.
```
Specifically, Flask has proven to be effective on real farms. Rathnayake (2024) used Flask to
```
develop a cloud-based system to collect and visualize agricultural data in a case study on
digital farming infrastructure in Sri Lanka. In the study, the aptness of Flask in limited
development environments is highlighted and its customizability and feature integration
simplicity are mentioned as its advantages. Such minimalist design is not only simpler to
develop but also helps the learners to better understand the system architecture, which makes
Flask a better option in academic applications such as AgriSense.
2.8.3 Data Ingestion and API Design
46
Figure 6: REST API
RESTful APIs are widely used as the back-end of agricultural IoT systems, where they are
used to receive data sent by field gateways and sensors. Such APIs provide a unified
communication paradigm using HTTP operations and JSON encoding to provide a reliable
and consistent way of sending data between different sensor nodes. In his introduction of a
```
climate-smart agriculture system, Aliche (2024) explains the use of REST-based APIs
```
through HTTP POST requests to receive sensor data, including soil moisture and
temperature, through ThingsBoard, and JSON to structure the payloads.
The REST APIs are preferable because of their simplicity, statelessness, and suitability with
```
mobile and web interfaces that are common in the agricultural sector. Aliche (2024) points
```
out that this architecture allows one to efficiently submit time-series data on many field
devices without needing complex protocols. Its scalability is assured by its uniform endpoint
design and robustness in unreliable rural network conditions is assured by built-in HTTP
error handling.
The quality and simplicity of data expansions are made easy by JSON payload validation and
```
endpoint design (e.g. /api/sensors/{id}/data) around domain routes. The system adopted by
```
```
Aliche (2024) demonstrates that RESTful ingestion pipelines may be integrated with cloud
```
dashboards and analytics services, establishing a consistent linkage between the acquisition
of real-time data and decision-making in precision agriculture.
47
2.8.4 Conclusion
In conclusion, the backend system of this agricultural IoT application is going to be layered
as it is more readable, modular, and fits the purpose of educational and research-oriented
development. This will make it maintainable, scalable and easy to collaborate by separating
concerns in the presentation, business logic and data layers. The choice of a programming
language is Python because it has embedded web development and machine learning
features, and Flask is a lightweight but flexible framework that allows rapid development and
deployment. JSON over HTTP-based RESTful APIs allow flexible and standardized
ingestion of sensor data in the field, with compatibility to mobile and cloud-based user
interfaces. This backend architecture allows a powerful, scalable, and easy to learn platform,
which can be used in precision agriculture.
48
2.8 Conclusion
The literature review reveals an increasing influence of IoT, cloud computing, machine
learning, and mobile development as a way to turn traditional agriculture into a data-driven
practice. These technologies make it possible to monitor in real-time, make predictive
analysis, and make responsive decisions, which are needed to enhance productivity and
sustainability, particularly in the rural, smallholder farming contexts. The proposed system,
AgriSense, based on the insights, was developed as a modular and scalable agricultural early
warning platform that can be used in academic development, as well as in the field in the
future.
Its design is based on the layered architecture of a Python-based Flask backend, which
processes sensor data, sends alerts, and combines machine learning models in AgriSense. The
choice of Microsoft Azure as a cloud platform supported by its educational assistance,
transparent cost, and integrated Internet of Things services such as Azure IoT Hub.
PostgreSQL is used to store data, as it is known to be scalable, and it is easy to connect with
web and cloud services. Random Forest, XGBoost, and MLP models are shortlisted to predict
the weather, whereas YOLOv5s, YOLOv7-tiny, and MobileNet-SSD-v2-Lite are shortlisted
to identify pests in real-time and with high accuracy and efficient performance.
Finally, because of the project limitations, namely, time, hardware availability, and the
budget, the system was tested within a simulated environment by using Ubidots STEM. It
enabled thorough testing of the data flow in real time, alerting, and model performance
without the need to implement physical IoT devices. Nevertheless, AgriSense platform is a
fully functional, deployment-ready system, providing a flexible and affordable precision
agriculture solution to underserved locations.
49
3.0 System Analysis
3.1 Introduction
This section of the report will give a thorough analysis of the proposed system, specifics of
the structure, functionality and flow of operations. This will contain a description of the
purpose and objectives of the proposed system, its architectural design and the breakdown of
visual representations such as use case and data flow diagram to aid in the description of user
interactions and movement of data with and within the proposed system. Moreover, SWOT
analysis will be conducted to discuss the strengths, weaknesses, opportunities and threats of
the system, to be sure of its feasibility and potential.
3.2 Proposed System
3.2.1 System Overview
AgriSense is a vision of a mobile-first product that will provide Malaysian smallholder
farmers with sophisticated tools to practice precision agriculture. On a fundamental level, the
system combines real-time collection of environmental data and advanced machine learning
as well as deep learning models to deliver predictive analytics and actionable insights. It
```
consists of the main parts, such as an easily accessible mobile app (Android and iOS), which
```
will provide the farmer with a platform for the application, a powerful backend application
```
(AgriSenseApp), which will be hosted on the Azure Cloud platform, and be used to process
```
data and run models, and a PostgreSQL database, which will provide a persistent storage of
sensor data, pest detection records, and user data. The system uses external cloud services
```
(UnifiedCloud) to retrieve weather and sensor data that is then converted to a standardized
```
time-series format. Analyze this data to draw predictions and anticipate threats and pest
detection models and weather prediction models. The system is incorporated with an alert
system whereby farmers are informed when there is an emergency and timely action is taken.
Also, the system will have options to report pests manually and an AI chatbot to interactively
assist farmers, which will form a complete solution that will help to reduce crop losses,
maximize input efficiency, and facilitate sustainable farming.
50
3.2.2 System Architecture
Figure 7: System Architecture Diagram of AgriSense
This architecture provides a full-fledged solution of agricultural monitoring through IoT
simulated sensor data, which seeks to provide farmers with real-time environmental data
collection, intelligent analytics, and actionable insights. The system employs multi-layered
architecture, which integrates hardware simulation, cloud computing, machine learning, and
easy-to-use interfaces to deliver weather warnings, pest identification, and advisory to the
farms.
The system is a modern example of an end to end solution of precision agriculture. The
architecture will enable farmers to make informed decisions based on data which can
potentially raise crop yields, reduce resource wastage and reduce environmental degradation
by combining the power of modern cloud computing and artificial intelligence with
traditional environmental sensing. The modularity will ensure that the system can be used in
diverse agricultural environments, including the family farms and large commercial farms. It
has 4 layers, perception layer, network layer, middleware layer, and application layer, and 2
extensions of Wokwi - Device Simulation and Ubidots STEM - Cloud Data Simulation.
51
3.2.2.1 Device Simulation Layer - Wokwi Platform
Wokwi is our hardware prototyping and validation platform, so it is not dependent on any
physical hardware. The platform has sensor emulators that allow testing of system behavior
with simulated environment sensors, an OV2640 camera simulator that allows validation of
image capture and processing flows, an ESP32 simulator that allows testing microcontroller
logic and sensor integration, and full logic and power tests that guarantee the reliability of
circuit design prior to physical deployment. This way of simulation shows compatibility of
the sensors and confirms hardware selection, showing that the chosen sensors can be
effectively integrated during the transition to actual IoT implementations.
The simulation environment is especially useful in the design and development stages, where
the team will be able to simulate the behavior of the system, verify data processing
algorithms and guarantee appropriate integration of various components without the cost and
complexity of hardware. The methodology saves a lot of time and money in development and
gives assurance that the selected sensors and microcontroller setups will behave as expected
in an agricultural setup.
3.2.2.2 Perception Layer - Physical Sensors and Devices
The perception layer reflects the hardware architecture that would be implemented in real-life
agricultural monitoring, showing the sensor capabilities and integration opportunities of
real-life agricultural monitoring. The suggested set of sensors is a DHT22 to measure
temperature and humidity to examine microclimate conditions, a Decagon EC-5 to measure
soil moisture to optimally schedule irrigation, a DS18B20 to measure soil temperature to
examine root zone conditions. Other environmental sensors are a TE525MM to measure
rainfall to monitor precipitation patterns, an Apogee SP-510 to measure solar radiation to
determine photosynthetic conditions, a Davis 6410 to measure wind speed to determine
weather patterns, and an OV2640 camera to provide a visual monitoring capability that
allows pest detection and crop health observation.
All these sensors would then be connected to an ESP32 microcontroller that acts as the
central processing unit of edge computing in a real deployment scenario. The ESP32 would
52
collect the data of the sensors, do some pre-processing to limit bandwidth requirements, and
handle communication protocols to send information to the cloud infrastructure. This edge
computing strategy would guarantee that important data processing can proceed even when
an intermittent connection is experienced, which is the case in distant farming areas. Local
decision-making of time-sensitive operations would also be performed by the microcontroller
and initiate immediate reaction to critical conditions before cloud-based analysis is done. In
this project, the Wokwi simulation tool will confirm the compatibility and integration
possibilities of these hardware components without any physical deployment.
3.2.2.3 Networking Layer - Communication Infrastructure
The networking layer offers a high quality communication infrastructure that is tailored to
agricultural settings that are not likely to have access to traditional connectivity. The system
involves LoRa transceivers that facilitate low-power and long-range communication suitable
in covering large agricultural farms without investing in huge infrastructure. LoRaWAN
gateway interconnects field devices to the internet, and LoRaWAN network server handles
device registration, data-routing, and network optimization to provide reliable
communications throughout the farm network.
The connection between the clouds is provided with the help of MQTT protocol that
guarantees the message delivery and efficient transmission of data even under adverse
network circumstances. Azure IoT Hub is an enterprise-level IoT platform to manage devices
and secure data ingestion that offers the scalability and security necessary to commercial
farming. The internet infrastructure offers a worldwide connection between the field devices
and the cloud services that make remote monitoring and management of the field devices
possible, which is a key requirement to provide the necessary precision in modern
agriculture applications.
.
3.2.2.4 Cloud Data Simulation - Ubidots STEM Platform
Ubidots STEM offers robust data simulation that is necessary in system development and
testing. The platform simulates realistic datasets of the environment to test the system,
simulates various data scenarios to effectively validate the system, and validates the model by
testing the machine learning solutions using synthetic data. This simulation environment
53
allows ensuring the reliability of a system before its deployment in the real world and allows
continuous testing of new functions without interfering with real agricultural activities.
The data simulation features are especially valuable to train the machine learning models and
test how the system would react to different environmental conditions that may not be
possible to appear naturally at the time of development. Ubidots STEM allows the
development team to test the system behavior in extreme conditions, to test the alert
thresholds, and make sure the user interface reacts properly to various kinds of agricultural
events and emergencies by offering controlled, repeatable test environments.
3.2.2.5 Middleware Layer - Azure Cloud Services
The system is based on the Azure cloud services that make up the data processing and storage
of the system. Azure IoT Hub is the main point of ingestion of all sensor streams of the
LoRaWAN network, authenticating the device and ensuring secure communications, and
scaling device-to-cloud messaging. The platform offers the device twin capability of remote
configuration, and the system administrators can change the sensor parameters and collection
frequencies without physically accessing the field devices. This is an essential factor in
sustaining and maximizing the performance of the system in distributed agricultural facilities.
Azure Stream Analytics offers the real-time data processing engine that can process incoming
sensor streams in real-time to analyze it immediately, to validate, filter, and transform data
and to raise real-time alerts when specific thresholds are reached. The service also collects
data for trend analysis and reporting, allowing both instant reaction and long-term
agricultural planning. The dual approach will provide timely warning to the farmers to take
immediate actions and at the same time create a complete database to provide strategic
decisions and planning of the season.
Database architecture focuses on PostgreSQL as the enterprise-level relational database to
store structured data, such as sensor readings with time stamp and device metadata, user
accounts and information about authentication, device registry and configuration data, and
history and logs of alerts. Geospatial database features, such as field boundary definitions and
geographic coordinates, location-based query optimization, and spatial analysis of zone-based
recommendations, and geographic correlation of environmental data are available through the
54
PostGIS extension. This geospatial capability is critical to precision agriculture situations
where geographic-specific advice can make a huge difference in crop yield.
3.2.2.6 Backend Service Architecture
The backend service is constructed on Python and Flask as the basic framework that
implements business logic, data processing schemes, integration with Azure services, and
custom algorithms of agricultural insights. This base provides stable data processing and
allows the deployment of complex agricultural algorithms that will be able to draw useful
information out of raw sensor data. The Flask framework offers the flexibility to incorporate
different Azure services with the desired performance level of real-time agricultural
monitoring.
FastAPI is the new, high-performance API layer that provides all the services such as
real-time sensor data endpoints, user authentication, and authorization, alert management
services, historical data query interfaces, geospatial field information services, and machine
learning prediction endpoints. FastAPI as a choice guarantees the high performance and
automatic API documentation which is essential to not only maintain but also scale the
system as it expands. The API design focuses on the real-time capabilities to access data
immediately and the extensive historical data analysis to plan agricultural activities in the
long run.
The integration of machine learning is accomplished with the use of Azure Machine
Learning, which offers a cloud-based ML platform to host trained models of detecting pests
and weather prediction, manage model versioning and deployment, and scale inference of
ML depending on the demand. TensorFlow integration allows deep learning in the processing
of images off the camera sensors, pattern recognition in the sensor data, and prediction
analytics in crop health assessment. This mix will make this system capable of using the
newest breakthroughs in the field of agricultural AI and still guarantee the scalability and
stability that are needed to conduct business.
3.2.2.7 Key Backend Responsibilities
55
The management of the data pipeline is one of the most important parts of the backend
infrastructure. The system should be designed and built to provide reliable data flow between
IoT Hub, Stream Analytics and database storage, provide data integrity and recovery in case
of communication failure, provide data transformation logic to accommodate various types of
sensors, and provide data partitioning and archival policies. This is a comprehensive data
management strategy that would ensure that no valuable agricultural data is lost and is
available at all times both in terms of immediate decision making and long term analysis.
The API design and development process aims at designing RESTful API endpoints that can
easily be integrated into mobile applications, developing effective data retrieval mechanisms
to handle historical data analysis, designing an API that can deliver notifications in real-time,
and securing APIs and rate limiting. The API is the essential connection point between the
cloud infrastructure and applications that will be exposed to users and therefore the design
and stability of the API is vital to the success of the system overall. The focus on efficiency
and security also guarantees that farmers are able to access their data fast and safely
anywhere.
The architecture of the alert system will convert machine learning forecasts into actionable
alerts, configure threshold-based warning systems, and develop alert prioritization and
escalation processes. The broad-based alerting mechanism will help to notify the farmers
about the important agricultural events in their preferred modes of communication and ensure
that the urgent cases are given due priority and attention.
Managing the field-boundary definitions and geographic metadata, the implementation of
location-based recommendation engines, the spatial query optimisation in large-scale
deployment, and the geographic visualisation data generation to use in mapping interfaces are
all part of geospatial services management. Such capabilities are needed in precision
agriculture applications where location-based insights can have a radical effect on agricultural
performance and resource optimization.
System integration guarantees the smooth communication of all the system components, error
handling and system resilience approach, monitoring and logging systems to have visibility
on operations, and automated test frameworks to continuously validate. Such a holistic
approach of integration guarantees the proper functioning of the multi-layered system and the
ability to detect and fix problems in a short time.
56
3.2.2.8 Application Layer - User Interfaces
Dialogflow AI chatbot offers a natural language interface to farmer queries, instantly
responding with weather alerts and pest warnings, providing personalised agricultural
recommendations and connecting to backend APIs to access real-time data. Such
conversational interfaces can make the system available to farmers with different degrees of
technical knowledge and offer an intuitive method of accessing complex agricultural
information and insights.
Its main user interface is the Flutter mobile application, which is a cross-platform solution to
both iOS and Android. The app includes a real-time dashboard and visualization of sensor
data, a system of push notifications that provide critical alerts, field mapping and geographic
data visualization, and an extensive set of historical data analysis and reporting tools. The
mobile-first strategy will make information that is vital to the farmers, available to them at
any point in their fields or on the road.
The API integration layer ensures that there is a secure communication between the frontend
applications and backend services, synchronization of data in real time across all user
interfaces, and data formatting and presentation standards. This layer of integration means
that the users will enjoy consistent and stable access to their agricultural data no matter which
interface they may prefer.
3.2.2.9 System Benefits and Future Considerations
The system has high scalability as the Azure cloud services allow elastic scalability to allow
multiple farms and thousands of sensors without infrastructure constraints. The cloud
redundancy and distributed architecture guarantees reliability, and continuous monitoring is
possible even when the hardware fails or network outages occur. The modular design is
flexible enough to support integration of new types of sensor and agricultural uses without
redesigning the system, and the pay-as-you-scale cloud model provides economic feasibility
of the solution to operations of all scales.
57
As the current project shifts gears towards implementation, a number of technical decisions
will have to be made, such as how to authenticate and authorize multi-tenant agricultural
processes, how to maintain data retention policies to balance cost-effective storage with data
analysis utility, and how to scale to the demands of high-volume sensor data during critical
growing seasons. Other factors are the methods of integration of new types of sensors and
agricultural machinery, and the conformity with agricultural data privacy and security
regulations. This architecture has the strength of creating a complete agricultural IoT solution
that will be able to scale to various farming activities without compromising performance,
security, and usability requirements.
58
3.3 Use Case Diagram
Figure 8: Use Case Diagram of AgriSense
The system supports three main actors who have different roles and responsibilities. The
main users who need full access to the agricultural data and tools of management are farmers
and Agriculture Agencies. Such actors should be able to observe the crop conditions, receive
alerts regarding possible problems, analyze the historical trends, and take relevant decisions
based on real-time and predictive data. Admins act as system administrators whose role is to
make sure that the platform is intact and users have appropriate access and that the system
59
settings are set properly so that the system can run efficiently and securely to all the users.
IoT Sensor Simulations are automated sources of input data that constantly provide
environmental and agricultural data to the system and simulate the presence of numerous
sensors in agricultural fields that measure the state of the soil, weather conditions, the state of
crops, and other essential farming indicators.
The functionality of the system starts with a full range of account management functions that
enable new users to create accounts and access the system using secure authentication
mechanisms. The users have the capacity to log out and log back in through a security
verification of passwords. In addition to basic access control, the system offers necessary
setup capabilities, where users may set up their profiles and details of farming operations in
terms of general information setup, whereas administrators may maintain user accounts and
set up system-wide parameters to ensure the best performance of the platform.
The AgriSense System has its core in strong data management and analysis capabilities. The
platform offers real-time viewing of information that allows users to access up to date
conditions and real-time data feeds of their farming activities. Historical data may also be
accessed by users in order to review past trends and patterns to make informed decisions
based on established trends and results. The system has the capability to import
environmental data which enables an external data source to be integrated with the system
and the administrators have the control of the imported datasets to maintain the quality of
data and the integrity of the system. Further, users will be able to report on any pests that are
not detected using a special reporting tool that will help the system identify and track pests.
The smart capabilities of AgriSense System make it a contemporary agricultural platform
with the incorporation of artificial intelligence and predictive analytics. Integrated weather
services allow the user to get information on weather forecasts, so they can plan in advance in
terms of farming activities. The system is an AI-based system that offers practical
recommendations depending on the current conditions and analysis of past data that can be
applied in specific farming scenarios. A chatbot consultation tool offers interactive support to
user requests and advice with the addition of uploading image features to create visual data
input to further monitor and analyze crop conditions and agricultural issues in depth.
60
The use case diagram discloses significant functional relationships in the system architecture.
The incorporated features in the login process are the password authentication and logout
feature, which guarantees secure access control. The core dashboard is the main interface and
it integrates several monitoring and reporting options and acts as the center of most user
activities within the system. Weather forecasting adds to the main dashboard experience with
the prediction of environmental information, and the AI chatbot adds to the simple
consultation with the ability to upload an image, which makes it possible to conduct more
complex analysis and suggestions.
61
3.3.1 Use Case Specification
Use Case ID UC001
Use Case Name Register Account
Description This use case allows new users to create an account in the AgriSense
System by entering the required personal and organizational
information, generating a username and password, and creating their
first profile to access the agricultural management system.
```
Actor(s) Farmer/Agriculture Agency
```
Precondition ● User has access to the AgriSense System interface
● User does not have an existing account
Postcondition ● The system creates a new user account
● Basic information is provided in user profile
● User is able to log in to the system
Basic Flow 1. User goes to the registration page
2. Registration form shown on system
3. User fills in necessary information ( name, email, contact details,
```
type of organization)
```
4. User chooses the type of account (Farmer or Agriculture Agency)
5. User designs username and password
6. Input data is validated in system
7. System opens new account
8. System notifies confirmation
9. Redirects user to log in page
Alternate Flow A1: Invalid Input Data
● 6a. System detects incorrect or incomplete data
● 6b. Error messages are shown on system when fields are invalid
● 6c. Information is corrected by user
● 6d. Resume from step 6
```
A2: Duplicate Account
```
● 7a. System identifies active account using same email/username
● 7b. Error message is shown in system
● 7c. User enters various credentials
● 7d. Resume from step 6
Exception Flow E1: System Error
● Technical problems are experienced, system fails to create
account
● Show error message and recommend to come later
62
Use Case ID UC002
Use Case Name Login Account
Description The use case enables registered users to log in with their credentials
and access the AgriSense System with the right type of permissions and
functionality related to their roles.
```
Actor(s) Farmer/Agriculture Agency, Admin
```
Precondition ● User owns a valid registered account
● System is available
Postcondition ● User is logged in to the system
● User enjoys proper role-based access
Basic Flow 1. User goes to log in page
2. System shows log in form
3. User puts in username/email and password
4. System authenticates credentials
5. System authorizes user
6. System creates a user session
7. Depending on role, System redirects user to dashboard
Alternate Flow A1: Invalid Credentials
● 4a. System reports the wrong username or password
● 4b. System shows error message
● 4c. User returns credentials
● 4d. Continue step 4
```
A2: Account Locked
```
● 5a. System identifies numerous unsuccessful logins
● 5b. System puts account on hold
● 5c. Account locked message is shown on the system
● 5d. User will have to wait or call admin
Exception Flow E1: System Authentication Service Down
● Show a message of display maintenance and the approximate
recovery time
63
Use Case ID UC003
Use Case Name Log Out
Description This use case allows users to securely end their system session,
ensuring all data is saved and the session is properly terminated to
maintain system security.
```
Actor(s) Farmer/Agriculture Agency, Admin
```
Precondition ● User is logged into the system
● Active user session exists
Postcondition ● User session is terminated
● User is logged out of system
● User is redirected to login page
Basic Flow 1. User clicks logout button/option
2. System confirms logout request
3. System saves any pending data
4. System terminates user session
5. System clears session data
6. System redirects user to login page
7. System logs logout activity
Alternate Flow A1: Unsaved Changes
● 3a. System detects unsaved changes
● 3b. System prompts user to save or discard changes
● 3c. User makes selection
● 3d. Resume from step 4
Exception Flow -
64
Use Case ID UC004
Use Case Name Setup General Information
Description This use case enables users to set up their profile with specific farming
operation information, preferences, and parameters that will be used to
personalize their experience and provide relevant agricultural insights.
```
Actor(s) Farmer/Agriculture Agency
```
Precondition ● User is logged into the system
● User has appropriate permissions
Postcondition ● User profile is configured with farming operation details
● System can provide personalized recommendations
● Dashboard displays relevant information
Basic Flow 1. User navigates to profile setup page
2. System displays setup form
3. User enters farm/operation details (location, crop types, farm size)
4. User configures notification preferences
5. User sets operational parameters
6. System validates and saves configuration
7. System confirms successful setup
8. System updates user dashboard with personalized content
Alternate Flow A1: Incomplete Information
● 6a. System identifies missing required fields
● 6b. System highlights incomplete sections
● 6c. User completes missing information
● 6d. Resume from step 6
Exception Flow E1: Database Connection Failure
● System cannot save configuration due to database issues
● Display error message and suggest trying again later
65
Use Case ID UC005
Use Case Name View Dashboard
Description This use case provides users with a comprehensive dashboard that
displays current agricultural conditions, alerts, notifications, and quick
access to various system features including weather forecasts,
recommendations, and real-time data.
```
Actor(s) Farmer/Agriculture Agency
```
Precondition ● User is logged into the system
● User profile is configured
Postcondition ● Dashboard displays current agricultural data
● User can access all included functionalities
● Real-time data is refreshed
Basic Flow 1. User accesses main dashboard
2. System retrieves user-specific data
3. System displays current conditions overview
4. System shows recent alerts and notifications
5. System presents navigation options to other features
6. System updates real-time data displays
7. User can interact with dashboard widgets
Alternate Flow A1: No Data Available
● 2a. System cannot retrieve current data
● 2b. System displays message about data unavailability
● 2c. System suggests troubleshooting steps
Exception Flow E1: Data Loading Timeout
● Dashboard data takes too long to load
● Display partial data with timeout notification
66
Use Case ID UC006
Use Case Name Check Weather Forecast
Description This use case provides users with comprehensive weather forecast
information including temperature, precipitation, humidity, and wind
data to help plan farming activities and make informed agricultural
decisions.
```
Actor(s) Farmer/Agriculture Agency
```
Precondition ● User is logged into the system
● Location information is configured
● Weather service is available
Postcondition ● Weather forecast data is displayed
● User can plan farming activities accordingly
Basic Flow 1. User requests weather forecast
2. System queries integrated weather services
3. System processes and formats weather data
4. System displays forecast information (temperature, precipitation,
```
humidity, wind)
```
5. System shows extended forecast period
6. System provides weather-based farming recommendations
Alternate Flow A1: Weather Service Unavailable
● 3a. External weather service is not accessible
● 3b. System displays cached weather data with timestamp
● 3c. System notifies user of service limitation
Exception Flow -
67
Use Case ID UC007
Use Case Name Receive Recommendations
Description This use case generates personalized agricultural recommendations
using AI algorithms that analyze current environmental conditions,
historical data, crop information, and farming parameters to provide
actionable insights for optimal farming decisions.
```
Actor(s) Farmer/Agriculture Agency
```
Precondition ● User is logged into the system
● Farm configuration is complete
● Sufficient data is available for analysis
Postcondition ● Personalized recommendations are generated and displayed
● User can act on provided recommendations
Basic Flow 1. System analyzes current conditions and historical data
2. System processes real-time sensor data
3. System applies AI algorithms for recommendation generation
4. System considers crop types and growth stages
5. System generates personalized recommendations
6. System displays recommendations with explanations
7. User reviews and can implement recommendations
Alternate Flow A1: Insufficient Data
● 1a. System lacks sufficient data for accurate recommendations
● 1b. System displays general recommendations
● 1c. System suggests data sources to improve recommendations
Exception Flow E1: AI Service Failure
● AI recommendation engine is unavailable
● Display cached recommendations with timestamp notification
68
Use Case ID UC008
Use Case Name View Real-time Information
Description This use case provides users with live monitoring capabilities,
displaying real-time data from IoT data including soil conditions,
environmental parameters, and crop health metrics for immediate
decision-making.
```
Actor(s) Farmer/Agriculture Agency
```
Precondition ● User is logged into the system
● IoT data simulation platform are active and transmitting data
● Data connection is available
Postcondition ● Current data is displayed and updated
● User has access to live monitoring information
Basic Flow 1. User requests real-time information
2. System queries active IoT sensor simulations
3. System retrieves current environmental data
4. System processes and formats data for display
5. System presents real-time dashboards and charts
6. System continuously updates data displays
7. System highlights any critical conditions or alerts
Alternate Flow A1: Simulation Data Unavailable
● 2a. Simulation platform not responding
● 2b. System displays last known values with timestamps
Exception Flow E1: Data Corruption
● Received data is corrupted or invalid
● Log error and exclude corrupted data from displays
69
Use Case ID UC009
Use Case Name View Historical Data
Description This use case enables users to access and analyze historical agricultural
data, providing insights into past trends, patterns, and outcomes that
support informed decision-making and long-term planning for farming
operations.
```
Actor(s) Farmer/Agriculture Agency
```
Precondition ● User is logged into the system
● Historical data exists in the system
● User has appropriate access permissions
Postcondition ● Historical data is displayed in requested format
● User can analyze trends and patterns
Basic Flow 1. User selects historical data view option
2. User specifies date range and data types
3. System queries historical database
4. System retrieves and processes requested data
5. System generates charts and trend analysis
6. System displays historical data visualization
7. User can export or further analyze data
Alternate Flow A1: No Historical Data
● 3a. System finds no data for specified parameters
● 3b. System suggests alternative date ranges
● 3c. System displays available data periods
Exception Flow E1: Data Corruption
● Historical database is inaccessible or corrupted
● Display error message and suggest contacting support
```
E2: Data Export Error
```
● System fails to export historical data
● Log error and suggest alternative export methods
70
Use Case ID UC010
Use Case Name Report Undetected Pests
Description This use case allows users to report pest sightings and activities that
may not have been automatically detected by the system. The system
analyzes reported pests using AI to identify new or previously
undetected species, contributing valuable field observations to the pest
tracking database and automatically improving the deep learning model
through retraining with new pest data.
```
Actor(s) Farmer/Agriculture Agency
```
Precondition ● User is logged into the system
● User has observed pest activity
● Reporting functionality is available
● AI pest detection service is operational
Postcondition ● Pest report is recorded in system
● Data contributes to pest tracking database
● New pest species are identified and logged
● Deep learning model is updated with new training data
● Other users may benefit from shared information and improved
detection
Basic Flow 1. User accesses pest reporting feature
2. System displays pest reporting form
3. User describes pest observations
4. User specifies location and crop affected
5. User uploads images if available
6. System validates and records report
7. System performs AI analysis on uploaded images and description
8. System compares findings against existing pest database
9. If new pest species detected, system logs as new discovery
10. System adds new pest data to training dataset
11. System schedules deep learning model retraining
12. System updates pest tracking database with all findings
13. System confirms successful report submission and any new
discoveries
71
Alternate Flow A1: Image Upload Issues
● 5a. Image upload fails or image is too large
● 5b. System provides error message and guidelines
● 5c. User adjusts image or continues without image
● 5d. Resume from step 6
```
A2: Known Pest Species Detected
```
● 8a. System identifies pest as existing known species
● 8b. System updates occurrence data for known pest
```
● 8c. System skips new species logging (steps 9-11)
```
● 8d. Resume from step 12
```
A3: AI Cannot Identify Pest
```
● 7a. AI analysis is inconclusive due to image quality or unknown
species
● 7b. System flags report for expert human review
● 7c. System stores report with "pending identification" status
● 7d. System notifies pest experts for manual classification
● 7e. Resume from step 12
Exception Flow E1: Database Storage Failure
● System cannot save pest report due to storage issues
● Display error message and suggest trying again later
```
E2: AI Analysis Service Down
```
● Pest detection AI service is unavailable
● Save report without AI analysis and queue for later processing
```
E3: Model Training System Failure
```
● Deep learning model retraining process fails
● Log training failure and schedule retry with system
administrator notification
72
Use Case ID UC011
Use Case Name Consult AI Chatbot
Description This use case provides users with an intelligent conversational interface
that can answer agricultural questions, provide guidance, troubleshoot
issues, and offer personalized advice using AI-powered agricultural
knowledge and contextual understanding.
```
Actor(s) Farmer/Agriculture Agency
```
Precondition ● User is logged into the system
● AI chatbot service is available
● User has specific questions or needs guidance
Postcondition ● User receives relevant assistance and information
● Conversation history is maintained for session
Basic Flow 1. User accesses AI chatbot interface
2. System initializes chatbot session
3. User types question or describes issue
4. System processes query using AI algorithms
5. System generates contextual response
6. System displays response to user
7. User can continue conversation or end session
Alternate Flow -
Exception Flow E1: AI Chatbot Service Down
● AI chatbot service is unavailable
● Display maintenance message and suggest alternative support
channels
73
Use Case ID UC012
Use Case Name Manage Users
Description This use case enables system administrators to create, modify, disable,
or delete user accounts, manage user permissions, and maintain overall
user access control to ensure system security and proper user
management.
```
Actor(s) Admin
```
Precondition ● Admin is logged into the system
● Admin has appropriate privileges
● User management interface is accessible
Postcondition ● User accounts are managed according to admin actions
● System maintains user access integrity
Basic Flow 1. Admin accesses user management interface
2. System displays list of user accounts
3. Admin selects user management action (create, modify, disable,
```
delete)
```
4. System displays appropriate forms or confirmations
5. Admin provides necessary information or confirms action
6. System validates admin permissions
7. System executes user management action
8. System logs administrative activity
9. System confirms action completion
Alternate Flow A1: Insufficient Privileges
● 6a. System identifies insufficient admin privileges
● 6b. System denies action and displays error message
● 6c. Admin contact higher-level administrator
Exception Flow E1: User Database Corruption
● User management database is corrupted or inaccessible
● Display critical error message and escalate to system
administrator
74
Use Case ID UC013
Use Case Name Configure System Settings
Description This use case allows system administrators to modify system-wide
configuration settings, parameters, and operational rules that affect all
users and system functionality, ensuring optimal platform performance
and customization.
```
Actor(s) Admin
```
Precondition ● Admin is logged into the system
● Admin has system configuration privileges
● System settings interface is available
Postcondition ● System configuration is updated
● Changes are applied system-wide
● Configuration changes are logged
Basic Flow 1. Admin accesses system configuration interface
2. System displays configuration categories
3. Admin selects configuration area to modify
4. System displays current settings and options
5. Admin modifies settings as needed
6. System validates configuration changes
7. System applies new configuration
8. System logs configuration changes
9. System confirms successful configuration update
Alternate Flow A1: Invalid Configuration
● 6a. System detects invalid or conflicting settings
● 6b. System displays validation errors
● 6c. Admin corrects configuration
● 6d. Resume from step 6
Exception Flow -
75
Use Case ID UC014
Use Case Name Manage Dataset Imports
Description This use case enables administrators to manage the imported datasets,
ensuring data quality, validation, and proper integration with existing
system data while maintaining data integrity and security standards.
```
Actor(s) Admin
```
Precondition ● Admin is logged into the system
● Admin has data management privileges
● Data sources are available
Postcondition ● Data is imported and integrated
● Data quality is maintained
● Import activities are logged
Basic Flow 1. Admin accesses data import interface
2. System displays available imported dataset options
3. Admin selects data source and import parameters
4. System validates data format and quality
5. Admin reviews data preview and confirms import
6. System processes and imports data
7. System integrates data with existing datasets
8. System logs import activity
9. System confirms successful data import
Alternate Flow A1: Data Quality Issues
● 4a. System identifies data quality problems
● 4b. System displays data quality report
● 4c. Admin decides to fix data or reject import
```
● 4d. If fixing, resume from step 4; if rejecting, end use case
```
Exception Flow E1: Storage Space Insufficient
● System lacks sufficient storage for data import
● Display storage error and suggest data cleanup or storage
expansion
76
Use Case ID UC015
Use Case Name Receive Alerts
Description This use case enables users to receive automated alerts and
notifications about critical agricultural conditions, weather changes,
pest activities, or system-detected issues that require immediate
attention or action.
```
Actor(s) Farmer/Agriculture Agency
```
Precondition ● User is registered in the system
● Alert preferences are configured
● System monitoring is active
Postcondition ● User receives relevant alerts
● User can respond to alert conditions
Basic Flow 1. System continuously monitors agricultural conditions
2. System detects condition requiring user attention
3. System evaluates alert criteria and user preferences
4. System generates appropriate alert message
5. System delivers alert through configured channels
6. User receives and reviews alert
7. User can acknowledge alert or take recommended action
Alternate Flow A1: Communication Failure
● 5a. Primary alert delivery method fails
● 5b. System attempts alternative delivery methods
● 5c. System logs delivery failure
● 5d. System retries alert delivery
Exception Flow -
77
Use Case ID UC016
Use Case Name Upload Image in AI Chatbot
Description This use case allows users to upload images during AI chatbot
consultations to provide visual context for their questions, enabling
more accurate analysis and recommendations based on visual
agricultural data such as crop conditions, pest damage, or plant
diseases.
```
Actor(s) Farmer/Agriculture Agency
```
Precondition ● User is in AI chatbot consultation session
● User has image to upload
● Image upload functionality is enabled
Postcondition ● Image is uploaded and processed
● AI can analyze visual data
● Enhanced recommendations are provided
Basic Flow 1. User initiates image upload during chatbot session
2. System displays file selection interface
3. User selects image file from device
4. System validates image format and size
5. System uploads and processes image
6. System performs AI-based image analysis
7. System integrates visual analysis with text consultation
8. System provides enhanced recommendations based on image
Alternate Flow A1: Invalid Image Format
● 4a. System detects unsupported image format
● 4b. System displays supported format list
● 4c. User selects appropriate image
● 4d. Resume from step 4
```
A2: Image Too Large
```
● 4a. System detects image exceeds size limit
● 4b. System suggests image compression
● 4c. User adjusts image size
● 4d. Resume from step 4
Exception Flow ● -
78
Use Case ID UC017
Use Case Name Import Environmental Dataset
Description This use case will enable the user to be able to import environmental
data into the system by connecting to external sources like weather
stations, soil sensors or third party agricultural databases to
complement the data analysis and decision making process in the
system.
```
Actor(s) Farmer/Agriculture Agency
```
Precondition ● User has logged into the system
● User is allowed to import data
● Supported format of environmental data is provided
Postcondition ● Imported environmental data can be analyzed
● Data is combined with already existing information
Basic Flow 1. The user accesses data import feature
2. System displays import interface
3. User selects environmental data file
4. System validates data format
5. System processes and imports data
6. System integrates data with user's agricultural information
7. System updates relevant dashboards and analyses
8. System confirms successful import
Alternate Flow A1: Unsupported Data Format
● 4a. System identifies unsupported data format
● 4b. System displays supported formats
● 4c. User converts data to supported format
● 4d. Resume from step 3
Exception Flow E1: Data Integration Failure
● System fails to integrate imported data with existing
information
● Log error and notify user of integration issues
79
3.4 Data Flow Diagram
Figure 9: Data Flow Diagram for AgriSense
3.4.1 Data Sources and Input Processing
This system begins the generation of data by an IoT Simulation Platform that generates
realistic sensor data that portrays the diverse agricultural parameters like the weather
conditions, soil measurements, and environment parameters. This simulated data is used as
the basis of all future processing and analysis in the system and it is used to test and develop
```
a controlled environment without the need to deploy physical sensors. Process 5 (IoT
```
80
```
Platform Management) is fed with data by the IoT Simulation Platform and is involved with
```
the coordination and management of the simulated sensor data infrastructure.
```
The raw data of simulation is validated by Process 6 (Input Validation) and is saved in the
```
```
IoT Simulated Data store (D1). At the same time, weather-related data are processed by a
```
```
specific Weather Prediction Model (Process 8), and pest-related patterns are processed by a
```
```
Pest Deep Learning Model (Process 9). These expert models convert raw environmental data
```
into useful predictive information, where validated pest image information is stored in the
```
Pest Image Data store (D4) to ensure data integrity in the system.
```
3.4.2 Machine Learning and Analytics Pipeline
The AgriSense system has core intelligence in its analytical abilities that are the key to how
```
the processed weather and pest information enter the analytical elements. Process 10 (Display
```
```
Weather and Pest Data) pulls together weather and pest data to display it, whereas Process 11
```
```
(Recommended Actions) will produce overall risk analyses and recommendations on actions
```
to take. This process of analysis is performed by machine learning algorithms to find patterns
and forecast possible agricultural threats.
The system has a unified risk management strategy whereby weather forecasts are integrated
with the probability of pest outbreaks to develop the pest and weather risk trigger elements
```
that can be used in the decision-making process. Process 12 (Alerts) deals with the
```
notification system that delivers important information to end users in a timely fashion using
multiple communication means. The analytical pipeline is a continuous processing of
incoming data to deliver real-time insights and ensure that risk assessments remain up to date
to agricultural stakeholders.
3.4.3 User Interface and Interaction Layer
The system has several categories of users such as Farm Owners and Agriculture Agencies,
which have customized access to system functions based on their needs and operating
requirements. The user interface layer includes the administrative and the end-user services,
which offer a complete platform of interaction with the system.
81
```
The administration processes are performed in two unique ways, Process 1 (Admin
```
```
Authentication) handles secure authentication of administrative user, Process 2 (Admin
```
```
Management) handles the administration of administrative account and configuration of the
```
```
system. In the case of regular users Process 3 (User Authentication) deals with the user login
```
```
credentials and authentication tokens and Process 4 (User Management) deals with user
```
account administration and access control. This segregation will provide adequate security
levels and role-based access within the system..
```
User services will be provided by an interactive AI Chatbot (Process 13) to resolve queries in
```
```
real-time, by providing the functionality to upload pest images (Process 7, Pest Image
```
```
Upload) to identify and analyze the image, and by displaying weather and pest data in detail
```
```
(Process 10, Display Weather and Pest Data). These services offer various ways of interaction
```
to the farmers and agricultural agencies to gain system insights and post appropriate
agricultural data.
3.4.4 Information Flow and Data Management
The system uses systematic data flow architecture in which data is passed through different
processing stages in logical order. The generation of data starts with creating simulated sensor
```
data by the IoT Simulation Platform which is then coordinated by Process 5 (IoT Platform
```
```
Management). The data are then validated by Process 6 (Input Validation) and later stored in
```
```
the corresponding data stores such as D1 (IoT Simulated Data) and D4 (Pest Image Data).
```
```
The application of machine learning models is performed by Process 8 (Weather Prediction
```
```
Model) and Process 9 (Pest Deep Learning Model) resulting in the display of consolidated
```
```
information by Process 10 and threat assessment by Process 11 (Recommended Actions). The
```
```
system has data stores D2 (Admin Data), D3 (User Data), and D5 (Weather and Pest Data) to
```
serve various functional needs and to enable efficient retrieval of data and system
performance.
3.4.5 Decision Support Capabilities
The Agrisense system is more of a decision support tool and not an automated control system
as it is important to rely on human expertise when making agricultural decisions. When the
82
```
Process 11 (Recommended Actions) identifies possible risks using its analytical activities, it
```
will provide recommendations that assist farmers in making informed decisions regarding
preventive pest management strategies, weather-related crop protection measures, the
optimum timing of agricultural activities, and resource allocation and planning decisions.
The decision support system offers contextual data and risk evaluations and enables
agricultural professionals to use their professional knowledge in making the final decision.
```
Process 12 (Alerts) will make sure that the critical information is delivered to Farm Owners
```
```
and Agricultural Agencies in time, whereas the AI Chatbot (Process 13) will allow making
```
inquiries and clarifications. This strategy will make sure that the system supplements instead
of replacing human judgment, which would be very useful in terms of providing crucial
information that can be used to make more efficient and timely decisions concerning
agricultural management.
3.4.6 System Integration and Scalability
The data flow architecture is modular and can be expanded in the future and integrated with
real IoT hardware, which is a sign of foresight in system design. Although in the present state
it works with simulated data using the IoT Simulation Platform, the architecture of the system
allows it to easily switch to the real world sensor integration without having to make
fundamental changes to the architecture, which provides the long-term sustainability and
flexibility of the system.
```
The separation of data processing (Processes 5, 6, 8, 9), analysis and presentation (Processes
```
```
10, 11, 12), user management (Processes 1, 2, 3, 4) and interactive services (Processes 7, 13)
```
provides maintainability of the system and the ability to scale different components
independently depending on the operational needs. This architectural style makes it easier to
modify and improve the system and be more stable and reliable in the core features.
83
3.5 SWOT Analysis
Strength Weaknesses
● Multi-platform compatibility across
mobile devices
The application is compatible with Android
and iOS operating systems, which makes it
accessible to a wide range of people
irrespective of their smartphone preferences
and can expand the rate of user adoption.
● Real-time agricultural hazard warning
system
The platform provides real-time warning
about weather conditions and pest activity so
that farmers can take timely action which can
greatly minimize crop damage and loss of
money.
● Easy to understand design based on user
backgrounds
The interface has visual icons, color coded
warning systems and less reliance on text,
which means that the interface can be used by
users with different literacy levels and
technical experience.
● Limited scope of functioning in
agricultural management
The existing system only targets weather
tracking and identification of pests without
essential agricultural factors like soil test,
field mapping, and nutrient management
monitoring.
● Lack of physical hardware implementation
The project is based solely on simulation
technology and does not use real IoT devices,
which ignores real issues in terms of
reliability, network connectivity, and field
installation conditions.
● Basic mobile device skills required
The users have to have basic knowledge of
operating a smartphone, which may not be
available to illiterate farmers who do not
have access or the basic knowledge of
operation of modern mobile technologies.
84
Opportunities Threats
● Possibilities of physical sensor network
integration
The framework will support the addition of
real IoT hardware such as ESP32
microcontrollers, DHT22 sensors, and soil
monitoring devices to gather a full set of data.
● Potentials of expansion into complete farm
management
It can be further extended by the system
architecture to have more modules such as
soil health assessment, crop lifecycle
monitoring, and harvest yield forecasting.
● The possibility of partnership with
governmental and non-governmental
organizations
There are opportunities available to
collaborate with government agencies and
non-governmental organizations that work on
agricultural development and offer channels
of broader distribution and institutional
support.
● Language adaptation for regional markets
The platform can be adapted to local
languages and dialects, especially Malay and
Tamil to serve the rural farming communities
and minimize the language barrier.
● Simulation could not be a complete
representation of the field conditions
Sensor delay, signal interference or hardware
failures cannot be simulated, potentially
concealing real-life hazards.
● Technological resistance
Conventional farmers can be reluctant or
even suspicious of digital tools.
● Existing commercial agricultural apps
Competition Competition
More established and large platforms might
have similar features but with more resources
and reach.
Table 3: SWOT Analysis of AgriSense
85
4.0 System Design
4.1 Introduction
This system design section of the report will present an extensive description of the different
designs in the proposed AgriSense agricultural monitoring system. These designs include the
user interface features such as the application logo and branding, and mobile application
screen designs that enable the farmer to interact with the system. The system design
documentation also includes detailed workflow diagrams of how various modules of the
system work, UML diagrams including class diagrams describing the object-oriented
structure of system components, state diagrams describing system behavior and transitions,
and sequence diagrams illustrating interaction patterns between different modules during
important operations, and tentative test plans with test design scenarios especially focused on
backend services and cloud infrastructure testing.
4.2 Interface Design
Figure 10: User Interface of AgriSense
86
Figure 11: Splash Screen, Sign Up Screen, and Login Screen
Splash Screen
The app opens with a simple and impressive splash screen that introduces the AgriSense
brand at once. It has the large green and gold leaf logo on a clean white background, which
represents the feeling of growth, nature, and modernity. AgriSense word mark is readable and
professional in its tone and informs the user about the identity of the application in a short
time. This screen is a quick introduction to the user before they are taken to the main
functionality.
Sign Up Screen
The Sign Up screen is simple and efficient in case of new users. It has a clear call to action:
Sign up to make crop management and field productivity easier. The fields are naturally
```
structured, asking the user to provide the basic information, i.e. name, email, password (and a
```
```
subsequent password field in case of password confirmation). The visual consistency of the
```
clean look of the splash screen is preserved. The main action is to create an account, which is
87
shown, in a nice green. There is also a clear option of logging in since there is an existing
user and this gives an alternative route.
Login Screen
The Login screen provides a simple journey to repeated users. It keeps the design of the app
clean with the fields of the email and password. A Forgot password? The option is easily
accessible to the convenience of the user. Under the main "Continue" button, AgriSense
```
cleverly adds social logins ("Continue with Google" and "Continue with Apple"), since the
```
user today favors faster and more convenient methods of authentication. Included in the list is
a prominent link of Sign up, so that those who do not have an account can easily switch
between the registration and the log in process. The footer is very discreet in assuring the
trust by providing links to Terms of Service and Privacy Policy.
88
Figure 12: Password Reset Flow Screens
Forgot Password Screen
It starts with a clean and concentrated Forgot password screen. The guidelines are very brief:
Please enter your email to reset the password. There is only one text field where the user
should enter his/her email address, and a big button Reset Password is available. The back
arrow in the top-left corner will enable the user to navigate easily back, increasing control.
Check Email Screen
The user is transferred to the Check email screen after sending his email. The message
conveyed by this screen is apparent that a 5-digit verification code has been sent to their
email address of their choice. The UI has separate fields to enter each code digit, and entering
data is fast and error-free. An entry is confirmed with a button labeled as a "Verify Code" and
a conveniently provided option to resend an email in case the user does not receive a code in
time to avoid frustration.
Set a New Password Screen
In case of successful verification, the user is brought to the screen of setting a new password.
This is a very important step that is informed by the security best practices, the message that
89
informs it to create a new password is prompted. Makes one create strong passwords, because
it says, ensure it is not similar to the earlier ones, to ensure security. There are two input
fields with visibility switches to make sure that the new password is correct: one says "Enter
your new password" and the other one says "Confirm your new password". The final
confirmation is reached through the visually consistent button, which is the green Continue
button.
Success Screen
The recovery process is ended by a reassuring Successful screen. The icon is large,
prominent, and a green checkmark, which communicates success, and then the message:
"Congratulations! Your password has changed. Click continue to log in." The cycle is then
closed by the user being redirected to the login page using the "Continue" button.
90
Figure 13: Home Screen, Settings Screen, and Notification Screen
Homepage
This central dashboard is the main operational summary for the farmer. It shows large sample
```
weather forecasts (e.g. temperature, conditions), showing where real time environmental data
```
would go. More importantly, there is an "Active Alerts" section that indicates emergency
```
cases, and it shows how weather warnings (such as thunderstorms) and pest identifications
```
will be delivered. The Current Status section is a short summary of important risk factors
```
(e.g. weather and pest risk), which allows a farmer to get a quick overview of the health of
```
their farm.
Settings Screen
This screen is created as a control center to users and thereby farmers can control their
AgriSense experience. Users are able to view their profile information, go to farm
```
management setup (to arrange sectors, crops and locations), and, most importantly, to access
```
91
notification options. It also has data import options and gives access to help and support
resources.
Notification Settings
This screen gives the farmers fine-grained control over their alerts and reminders. It has
```
toggles to general push notifications and individual weather-specific warnings (e.g., rainfall
```
```
and drought) to show how farmers can tailor proactive alerts based on the machine learning
```
models of the app. To alert the user of the detection of a pest, there is a pest detection alert
toggle so that one can get notifications as soon as the computer vision model detects a threat.
92
Figure 14: Farm Management Screen, Import Dataset Screen, AI Chatbot Screen
Farm Management Screen
This screen enables farmers to be able to effectively plan and view the structure of their farm.
```
It enumerates sample farm sectors (e.g., "Sector A - Rice Field," "Sector B - Vegetables
```
```
Field") that show major information such as location, area and the crop that is planted and the
```
date. With the help of this interface, farmers can control the various sections of their land and
crops, and each of these sectors has an edit icon that allows them to control their farm in the
app. In addition, there is a distinct button allowing the user to add a new section to their farm
to further develop its online representation in the app.
Import Dataset Screen
This prototype screen was created to be flexible and provide superior understanding, which
means that the user can upload his or her own weather or pest data. The interface also has a
clear upload field, data type selection option, and date range specification fields so that
93
farmers can customize information to analyze individually and to optimize the app. This
characteristic underscores AgriSense extensibility on specific user details.
AI Chatbot Screen
This screen presents the AI farming assistant of AgriSense. It is shown as a conversational
```
interface, and displays sample historical interactions in which users pose questions (e.g., How
```
```
do I control the Asiatic rice borer?) and get intelligent, context-sensitive answers and advice.
```
There is an input field where farmers can type in their question: Ask your question and the
query bubbles provide guidance. There is also an option to upload images, so that farmers can
instantly acquire feedback. This attribute is expected to offer immediate and informed
assistance, and it will be able to directly answer the questions of farmers on the move.
94
Figure 15: Weather Details Screens
Current View of Weather Details
```
This screen displays real-time environment data on a chosen farm sector (e.g. "Sector A -
```
```
Rice Field"). It shows important values of temperature, humidity, rain, wind speed, solar
```
radiation, weather condition, soil temperature, and soil moisture. The real-time summary
assists farmers in comprehending the status of the fields, which becomes an essential aspect
in day-to-day decision-making. The tab bar is prominent and allows users to switch between
the Current data, Forecast data and Historical data to access different functionalities to
provide farmers with the information they need.
Weather Details - Select Sector
Being a part of the weather module, this screen enables effective multi-sector management. It
```
enables farmers to choose a certain farm sector out of a list (e.g. "Sector A - Rice Field,"
```
```
"Sector B - Vegetables Plot," "Sector C - Corn Field"). Once you select an area, the weather
```
information in the other tabs will dynamically change to provide the environmental
conditions of the selected area, which provides precise and accurate location-specific
information.
95
Forecast View - Weather Details
This is a strong forecaster screen that gives the farmers proactive planning tools. It shows
```
sample "Recommendation Actions" that are based on the predicted conditions (e.g.
```
```
recommendations on pest control or irrigation). Under this, there is an Hourly Forecast and a
```
7-Day Forecast that shows expected weather conditions with the degree of confidence, and
farmers can adjust to upcoming changes in rainfall and temperature and other weather factors.
Weather Details - Historical View
This screen provides access to historical environmental information in order to do a
long-term analysis and strategic planning. It has a date range control to define the time of
```
interest. Past data is clearly shown in a graph (e.g. "Historical Temperature Trends") and past
```
```
insights are displayed in a simplified form (e.g. averaged temperature over a time). This
```
aspect allows the farmers to have knowledge of the climatic patterns, past decisions and
future trends depending on history.
96
Figure 16: Pest Alerts and Details Screen, Control Recommendation Screen
Pest Alerts Log Screen
This screen acts as the main control center of all pest related threats in the farm. It provides a
```
clear record of sample pest alerts, with each line containing the name of the pest (e.g., "Stem
```
```
Borer," "Rice Leaf Folder"), the farm sector in which it was detected and the time when it
```
was detected. These alerts can be easily filtered by the user using All, Active, Resolved, or by
Sector to create a focused management. This log is meant to provide the farmers with a
general scope of the pest activity on their whole farm.
Alert Details Screen
When a certain alert is selected, this screen will display a detailed analysis of the detection. It
also shows clearly the sector in which the pest was identified and the time of identification.
```
Most importantly, it shows the image that caused the alert (e.g. an image of a Stem Borer) so
```
that the farmer can see the threat with his own eyes. The confidence level of the detection by
97
```
the AI is also displayed on the screen and a clear risk assessment (e.g. High Risk - Immediate
```
```
Action Recommended) lets the farmer know what action to take. There are easy ways to
```
"View Control Recommendations," "Mark as Resolved," or "Report False Positive," making
the work process much easier.
Control Recommendations Screen
This very practical screen turns detection into action. It offers multi-faceted control
```
recommendations to the identified pest (e.g., "Stem Borer") that are divided into three
```
categories, namely, "Chemical Control," "Physical Control," and "Biological Control." All
categories include detailed recommendations of products/methods, dosage, time of
application, tools required, and frequencies. Here the AI Confidence level of the first
detection is also indicated clearly. Such extensive advice enables farmers to select the most
appropriate intervention measure to reduce the damage caused by pests.
98
Figure 17: Report Pest Screens
```
Report Pest Screen (First Screen)
```
This screen is a clean, self-explanatory interface to post a manual pest report. It starts with the
"Location Details" with a drop down to the "Select Sector" that enables farmers to identify
the very location of their farm where the pest was detected referring back to their farm
management arrangement. Thereafter, a large and clear "Upload Photo" section with an icon
of the same name allows farmers to take a photo of the pest or diseased crop or to upload an
image to the report and thus present crucial visual material. There is a dropdown to select the
99
```
type of pest, (further explained in the second screen) and the farmer can add a description
```
box, any textual information that they may have concerning what they have observed before
they can complete the submission by clicking a clear button marked as Submit Report.
```
Pest Type Selection (Report Pest Screen)
```
This is the screen that features the user interaction in choosing the type of pest. On tapping
```
"Select Pest Type" dropdown, a predefined list of common agricultural pest (e.g. "Stem
```
```
Borer," "Aphids," "Rice Leaf Folder," "Leaf Miner") appears. There is also an option of an
```
Other, which allows the flexibility of reporting less frequent or unnamed pests. This
systematic selection makes the reporting process easier and assists in classifying observations
to maintain records.
100
4.3 Workflow of Proposed System
Figure 18: Workflow of AgriSense
AgriSense system has a user-friendly and interactive workflow with a clearly defined path of
the farmer using the application since his first access to the application to advanced
management of the agricultural system. The whole process starts with an entry point of the
user, on whether the individual is a new user or not. The system directs new users through a
registration process which it checks to ensure that it is successfully completed. Once a
successful registration has been done, or in the case of returning users, the login process then
101
begins, and the system will verify the credentials to provide access. After successfully
logging-in, the farmer instantly gets into the environment of the application and can get any
pending alerts, which preconditions proactive interaction.
There are a few important actions that can be made by the farmer through the main menu.
They can explore the "Setup Settings" to customize their experience, and any change is
confirmed by the system prior to being confirmed. Alternatively, farmers may use AI Chatbot
to get immediate farming advice, and they may also attach pictures to get more specific
questions, the system will analyze the questions and provide a response to the farmer. In
addition to these, the main menu also acts as a portal to opening the View Dashboard, which
is a hub of information on detailed farm insight.
In the dashboard, as well as other navigation channels, the farmer is able to choose particular
widgets to learn more about their farm. They are able to see live environmental data, an
ability which causes the system to call sensor data in real time. Historically, farmers will have
an option of accessing historical information by letting the system do the retrieval of the
historical information. An important manual input facility will enable farmers to report pests
that have not been detected and they will be able to upload images to accompany their report
which is then stored by the system. Moreover, the farmer has an opportunity to directly view
the weather forecast or the active alerts, going into the details of the alerts and as a result,
being provided with the personal recommendations based on the analytical processes of the
system.
The AgriSense system is in the process throughout all these interactions. The internal
processing is triggered by every farmer action, such as viewing the data, submitting reports,
or consulting the AI. One of the basic background processes is to conduct continuous data
analysis, use sophisticated calculations, machine learning algorithms, and deep learning. The
continuous evaluation produces results, outputs and further recommendations which are then
fed back to the farmer completing the loop of knowledge and action. This unified process
guarantees that AgriSense offers an open-ended and engaging solution to data-driven farm
management.
102
4.4 UML Class Diagram
Figure 19: Class Diagram of AgriSense
The class diagram is an all-inclusive object-oriented architecture that contains 12 classes that
outline the static architecture of an agricultural monitoring and forecast system. Every class
shows good encapsulation with well defined attributes and methods and forms a good
foundation with well organized relationships and dependencies to ensure scalable agricultural
technology implementation.
```
The central domain entity is the User class that has seven attributes (userID, name, role,
```
```
phone, email, location, cropType) and six methods (login, logout, updateProfile,
```
```
uploadImage, viewAlerts, viewPredictions) creating the main user interactive actions. The
```
103
client-side interface is encapsulated into the MobileApp class with three attributes
```
(appVersion, deviceID, operatingSystem) and five methods (sendImage, displayAlerts,
```
```
displayPredictions, syncWithBackend, fetchTrendData) that provides the primary user
```
interface with the system.
```
The AlertSystem handles the notification based on four attributes (alertId, type, message,
```
```
severity) and four methods (generateAlertMessage, notifyUser, logAlert, sendAlert) and
```
offers full functionality on alert management. Two classes specialized in cloud infrastructure
```
are offered, AzureCloud with two attributes (cloudProvider and services) and four methods
```
```
(deployApp, monitorResources, scaleServices, storebackup) and UbidotsCloud with two
```
```
attributes (apiEndpoint and apiKey) and three methods (simulateWeatherData,
```
```
simulateSensorData, sendToBackend). The AgriSensorApp (Backend) is the IoT integration
```
```
layer that has contains three attributes (appID, status, hostLocation) and six methods
```
```
(fetchSensorData, storeToDatabase, triggerAlert, runPestPrediction, runWeatherPrediction,
```
```
handleUserUpload), which takes care of sensor data processing and prediction coordination.
```
```
The PostgreSQLDatabase class handles data persistence, with three (dbName, sqlUser, host)
```
```
parameters and four (storeData, retrieveData, updateRecord, deleteRecord) operations, which
```
forms the data baseline of the system. The representation of environmental data is managed
in terms of 2 inter-related classes and then transmitted to a class that provides temporal
```
organization: WeatherData with four attributes (rainfall, temperature, windSpeed,
```
```
forecastDate), SensorData with four IoT measurements (temperature, humidity,
```
```
solarRadiation, soilMoisture), and then sent to TimeSeriesData class that provides temporal
```
```
organization with five attributes (timeStamp, sensorType, value, unit, source) and four
```
```
methods (getLatestData, getHistoricalData, filterBySensorType, gatherData).
```
The system predictive capabilities are implemented in two specialized model classes.
```
WeatherPredictionModel has two attributes (modelVersion, parameters) and three methods
```
```
(predictWeather, fetchInputData, generateForecast), whereas PestPredictionModel has two
```
```
attributes (modelVersion, imagePath) and four methods (detectPest, predictPestRisk,
```
```
getPredictionResult, loadTrainingData), and it is clear that the machine learning logic is
```
separated from data representation.
104
4.5 UML State Diagram
4.5.1 User Session Lifecycle
Figure 20: State Diagram - User Session Lifecycle
The state diagram of the User Session Lifecycle provides a detailed representation of the flow
of a user in the AgriSense application starting at an Idle state. When a user clicks on a
"Login" action, the session sends them to the Entering Credentials where he is required to
enter his details. When the user proceeds with Submitting Credentials, the system switches to
Validating Credentials and depending on the result, either switches back to Entering
Credentials in case of a Login Failed or goes to Logged In Successfully in case of Login
Success. After a successful log in, the user may choose an option which is "Select Dashboard
Feature" and this will be the beginning of the Interacting With Dashboard state which means
that the user is now actively using the functions of the application. Lastly, the session will end
when the user takes a Log out action, and the status of the session will be changed to the
Logged out state, which will end the active presence of the user.
105
4.5.2 User Registration Flow
Figure 21: State Diagram - User Registration Flow
The state diagram above shows the User Registration Flow, it shows the whole procedure that
a new user goes through to create an account in AgriSense. The flow starts at Idle state and
when the user clicks the action to "Register", the user enters into the Filling Registration
Form state. After the user has filled in his details and decides to click on the button of
submitting the form, the system moves to Validating Input so as to make sure that the
information given is as per the requirements. In case of Validation Unsuccessful, the flow
returns to the Filling Registration Form and the user is told to correct the errors. On the
contrary, when it comes to Validation Successful the system moves to Saving User Data.
Lastly, after the completion of the Save Data event, the registration is successfully concluded
in the Registration Complete state, and the user has successfully been created with an
AgriSense account.
106
4.5.3 Dashboard Interaction
Figure 22: State Diagram - Dashboard Interaction
The state diagram of Dashboard Interaction defines the dynamic interaction of a user
AgriSense after the Dashboard is Loaded and arrives at the main hub of the multiple services.
Based on this loaded status, the user may choose Viewing Real-Time Environmental Data by
clicking on the relevant option or may embark on a process to Uploading Pest Image, which
in turn leads to Validating Image Input, in case of failure of validation, the user returns to
uploading, though in case of "Validation Passed," the process is continued to Viewing Alerts.
The user is also able to go directly to the Viewing Alerts state via the Dashboard through
"Receives Alert Notification". Additional communications contain Viewing Historical Data
or Viewing Weather Forecast that are available through selection in the dashboard. Finally, a
user has an option to trigger Chatbot Consultation, which results in the Chatbot Session
Active status. All these sub-features enable the user to go back to the Dashboard Loaded
state, ensuring a smooth navigation process, which shows that the dashboard is the central
point of all the operations.
107
4.5.4 IoT Data Handling Simulation
Figure 23: State Diagram - IoT Data Handling Simulation
The state diagram of the IoT Data Handling and Simulation shows a backend flow of how
AgriSense receives incoming sensor data and ends with creating alerts. The flow starts at a
Waiting Data Input state and waits on information. When it receives Simulated Data, the
system transitions to Processing Incoming Sensor Data where the data is prepared to undergo
integrity checks. This results in the state of Validating Sensor Payload, if the validation is
unsuccessful, the process returns to Processing Incoming Sensor Data to be evaluated again.
On the other hand, when the message is Validation Successful, the data is passed onto Saving
Data to Database, after which it gets into the Data Ready For Visualization state when the
Data is Saved Successfully. Lastly, the System Alert Generated is triggered by the processed
data when a threshold is reached, it switches to Triggering Alert Notification, which means
that an alert was initiated successfully to the user.
108
4.5.5 Admin Management
Figure 24: State Diagram: Admin Management
The state diagram of the administration management represents the specific workflow of
administrative users in AgriSense with emphasis on user and system settings. The process
usually starts in a Dashboard Loaded state in which an administrator can click on an Open
User Management to move into the Managing Users state. Here, the administrators can Adds
New User, which takes to Validating User Input, in case of Validation Unsuccessful, it takes
to Managing Users, and in case of Validation Successful, it takes to Saving New User, and
after a user is created it goes back to the Managing Users state. Also, on Managing Users
state, administrators have the option of clicking on the Edit Or Remove User which results in
Update User Records and once the action is completed they move back to Managing Users.
By clicking on the state of the Managing Users, administrators can also access Managing
System Settings by clicking on Open System Settings and can also navigate Back to
Managing Users or Dashboard Loaded by clicking on Managing System Settings, indicating
that the work of administration is done.
109
4.6 UML Sequence Diagram
4.6.1 User Login Flow
Figure 25: Sequence Diagram - User Login Flow
The sequence diagram of the User Login Flow describes in detail the step by step process of
interaction between the user and the system elements of AgriSense in the process of
authentication. The flow starts with the User entering his/her username and password into the
Login Interface, which in its turn sends this "login request with credentials" to the
Authentication Controller. The Authentication Controller then "queries the user record by
username/password" with the User Database and in turn returns the authentication result to
the controller. According to this outcome, the flow branches into the case where the login is
successful, the Authentication Controller "returns success status" to the Login Interface,
which in turn "loads the user-specific dashboard" to the User and also communicates with the
Dashboard Interface to "load dashboard", in the case where login fails, the Authentication
Controller "returns failure status" to the Login Interface, which proceeds to "display an error
message" to the User, thus ending the authentication process.
110
4.6.2 Upload Pest Image and Get AI Feedback
Figure 26: Sequence Diagram - Upload Pest Image and Get AI Feedback
The sequence diagram of the Upload Pest Image and Get AI Feedback gives a description of
how a user uploads a picture of a pest and gets AI-based feedback. The process of interaction
starts with the user choosing and uploading a pest image via the Dashboard Interface where
the image is then instantly "sent to the validation stage" to the Validation component. After
this validation, the flow is branched to the case where if the image is valid, the Validation
component will send the message of the validity to the Dashboard Interface, and the latter
will send the message to AI Engine that the image is to be analyzed by the AI, and the AI
Engine will send the message of the analysis result with recommendation to the Dashboard
Interface and the message of the image and the result of the AI analysis will be stored in the
Database, and the Dashboard Interface will display the message of the recommendation and
the result to the User. On the other hand, if the image is not valid, then the Validation
component merely returns the invalid status to the Dashboard Interface which goes ahead and
shows an error message to the User, and the process ends with that specific image
submission.
111
4.6.3 Viewing Dashboard Data and Alert
Figure 27: Sequence Diagram - Viewing Dashboard Data and Alert
The sequence diagram named Viewing Dashboard Data & Alert demonstrates the complex
procedure according to which AgriSense delivers different kinds of important data to the user
via the dashboard interface. When the User visits the dashboard, the Dashboard Interface
makes a "Request real-time data" to the Data Fetching component, which in turn "queries to
get real-time sensor values" to the Database, in case where data is found, real-time data will
be displayed, otherwise an error message showing no sensor data. Equally, the Dashboard
Interface can request historical data, which causes a query with the Database of past record,
112
producing either the historical dataset to be presented as charts and history, or stating there is
no history. Moreover, the Dashboard Interface is capable of requesting current alerts to the
Alert System, which queries the Alert System to the Database, and in case alert records are
returned, pest/weather alerts are shown, otherwise the message “No new alerts” is displayed.
Lastly, the User can then engage with these alerts that are displayed by acknowledging or
dismissing them through the Dashboard Interface, thus concluding the data viewing and
interaction process.
113
4.6.4 IoT Simulation Data Flow
Figure 28: Sequence Diagram - IoT Simulation Data Flow
The IoT Sensor Simulation Data Flow sequence diagram displays the step-by-step diagram of
how simulated environmental sensor data is processed in AgriSense, after being created by a
user, through to its eventual storage and user feedback. The flow starts by the User triggering
environment data simulation by clicking on the IoT Simulator Interface, which subsequently
sends raw simulated sensor data to the Data Validation component. After such a validation,
the process forks into if the data is valid, Data Validation will report valid status to the IoT
Simulator Interface, which will report validated sensor data to the Data Processor, the Data
Processor will report processed environmental data stored to the Dashboard Data Store, and
report success of data storage back to the IoT Simulator Interface, which will report
successful data import to the User. On the other hand, in case if the data is invalid, Data
Validation will send back an invalid status to the IoT Simulator Interface, which will in turn
send an error message to the User, and the simulation process is over.
114
4.6.5 Admin Managing User and Settings
Figure 29: Sequence Diagram - Admin Managing User and Settings
The Admin Management sequence diagram displays the unique flow of administrative users
in AgriSense, where the emphasis is on the user account management and configuration of
the system-wide settings. Through the Admin Dashboard Interface, an administrator has the
option to manage users, which triggers a request to the User Management component to
request user data, which then retrieves and presents a list of users. The administrator may
then choose to add, edit or delete a user, this request is forwarded to the User Management,
which in turn processes the request by updating the user record in the Database and
acknowledges the request back to the interface with a confirmation message. Alternatively, an
administrator can open system settings through the Admin Dashboard Interface. This will
pass on the new configuration to the System Settings component that will save the new
settings in the Database and acknowledge the save displaying a success message to the
administrator thereby concluding the administrative task.
115
4.7 Test Plan
AgriSense backend and cloud infrastructure testing aims at providing efficient server-side
operations, stable data processing, safe API endpoints, and data integration using cloud
services. The main tasks are: to verify the integrity of the data throughout the processing
pipeline, to verify that the communication between backend services is seamless, and to
verify that the system can perform agricultural data workloads efficiently with different
conditions.
4.7.1 Levels of Testing
Unit Testing
Unit Testing concerns the singular functions in the backend such as API route handlers, data
transformation functions, authentication functions, and database query functions. The
individual components are tested in isolation to ensure that they are being processed
correctly, errors handled appropriately and business logic is correct.
Integration Testing
Integration Testing checks the communication among various backend services, database,
external API integration, and cloud services. This makes sure that data moves properly
throughout the whole processing pipeline sensor ingestion to final storage.
System Testing
System Testing tests the entire backend infrastructure in real-world conditions, such as
parallel user connection, end-to-end data processing pipelines, and resource-consuming batch
tasks, such as training AI models and generating reports.
Cloud Infrastructure Testing
Cloud testing incorporates reliability of database services, auto-scaling configurations,
operations of the storage services, and Content Delivery Network performance. This
comprises the verification of the back-up procedures, disaster recovery systems, and the
ability of the system to support the peak season of agricultural monitoring activities by
providing the right amount of resources.
116
4.8 Design Test Scenario
4.8.1 API Endpoint Testing
Authentication and Authorization
Authentication and Authorization testing verifies that the user can successfully log in with
valid credentials and fail with invalid credentials, token generation and expiry, and role-based
access control to make sure that a user can only access relevant information and functionality
with their respective roles.
Data Processing Endpoints
The Data Processing Endpoints are tested using sensor data of different formats and payloads
to make sure that ingestion, storage, and response processing are appropriate. Different
uploads of images and environmental data are used to validate AI prediction endpoints to
ensure correct results can be achieved within acceptable response time.
4.8.2 Database Operations
CRUD Operations
CRUD Operations testing will ensure that insertion, retrieval with different query parameters,
updating of profiles and deletion of sensor data do not break referential integrity. Transaction
management makes multi-step operations succeed or roll back entirely in case of failures.
Data Integrity
Data Integrity testing confirms that sensor data is within the normal range, that relationships
between data items are not broken, and that aggregate calculations such as the averages are
not broken as new data is added.
4.8.3 Cloud Service Integration
External Weather API Integration
External Weather API Integration testing includes the success of the data retrieval in normal
circumstances, the error response when APIs are not available, and the rate limiting that must
comply with the suitable retry mechanisms in the case of service restrictions.
117
Cloud Storage
Cloud Storage testing confirms file uploads of different sizes and formats, effective
accessibility to AI and user downloads, and the backup/recovery procedure to guarantee that
the files can be restored promptly when services are disrupted.
4.8.4 Performance and Scalability
Load Testing
Load Testing emulates the situation when several farmers use the system at the same time
when it is busy, tracking API response time and database performance. Stress testing locates
breaking points of the system and proves out graceful degradation mechanisms.
Data Processing Performance
Data Processing Performance gives the capability of the system to work with high volume
sensor data and at the same time have real time user responsiveness. Performance testing of
AI models evaluates that machine learning predictions remain accurate when the service is
subject to concurrent requests.
4.8.5 Security Testing
Data Security
Data Security authenticates data in transit and at rest encryption, SSL/TLS certificate settings,
and database access authentication. Testing makes backup and recovery processes to be
within the standards of encryption.
API Security
The API Security encompasses testing against SQL injection, cross-site scripting attacks, rate
limiting protection, and DDoS security to make sure that the system can differentiate between
a legitimate use and a possible attack and keep the service available.
118
Reference
1. Sauvagerd, M., Mayer, M., & Hartmann, M. (2024). Digital platforms in the
agricultural sector: Dynamics of oligopolistic platformisation. Big Data & Society,
```
11(4). https://doi.org/10.1177/20539517241306365
```
2. Goodman, C., Simonson, A., Oyler, J., & Dissen, J. (2021, May 21). Open data on
AWS supports sustainable agricultural practices and crop optimization. Amazon Web
Services.
```
https://aws.amazon.com/blogs/publicsector/open-data-aws-supports-sustainable-agric
```
ultural-practices-crop-optimization/
3. Miller, T., Mikiciuk, G., Durlik, I., Mikiciuk, M., Łobodzińska, A., & Śnieg, M.
```
(2025). The IoT and AI in Agriculture: The Time Is Now—A Systematic Review of
```
```
Smart Sensing Technologies. Sensors, 25(12), 3583.
```
```
https://doi.org/10.3390/s25123583
```
4. Miller, J., & Shekhar, S. (2024). Cloud computing in smart agriculture: data storage,
processing, and analysis. ResearchGate.
```
https://www.researchgate.net/publication/389490976_Cloud_Computing_in_Smart_A
```
griculture_Data_Storage_Processing_and_Analysis
5. Bhalekar, N. (2.24). Benefits of running databases on Amazon Relational Database
Service over traditional on-premises servers. International Journal for
```
Multidisciplinary Research (IJFMR). https://www.ijfmr.com/papers/2024/2/16795.pdf
```
6. MDW Srimal, MSM Aboobucker, HH Shaikh et al. (2024). IOP Conference Series:
```
Earth and Environmental Science, 1401(1), 012004.
```
```
https://iopscience.iop.org/article/10.1088/1755-1315/1401/1/012004/pdf
```
7. Daniel, S., Brightwood, S., & Oluwaseyi, J. (2024). Cloud-Based Big Data Analytics:
AWS, Azure, and Google Cloud.
```
https://www.researchgate.net/publication/385885475_Cloud-based_big_data_analytic
```
s_aws_azure_google_cloud
8. Ojika, F. U., Owobu, W. O., & Abieba, O. A. (2023). Transforming Cloud Computing
```
Education: Leveraging AI and Data Science.
```
```
https://www.researchgate.net/publication/390840481_Transforming_Cloud_Computin
```
g_Education_Leveraging_AI_and_Data_Science_for_Enhanced_Access_and_Collab
oration_in_Academic_Environments
9. Dauda, A., Flauzac, O., & Nolot, F. (2024). A Survey on IoT Application
```
Architectures. Sensors, 24(16), 5320. https://www.mdpi.com/1424-8220/24/16/5320
```
10. Thilakarathne, N. N., et al. (2022). A Cloud-Enabled Crop Recommendation Platform
```
for Machine Learning-Driven Precision Farming. Sensors, 22(16), 6299.
```
```
https://www.mdpi.com/1424-8220/22/16/6299
```
11. Morchid, A., Marhoun, M., El Alami, R., & Boukili, B. (2024). Intelligent Detection
for Sustainable Agriculture. Multimedia Tools and Applications.
```
https://link.springer.com/article/10.1007/s11042-024-18392-9
```
12. Pereira, R. H. (2024). Lightweight data bridge for connecting self-service end-user
analytic tools to NGSI-based IoT systems. Internet of Things, 25, 101125.
```
https://doi.org/10.1016/j.iot.2024.101125
```
119
13. Hess, P. T. (2022). Building a Spatial Database for Agricultural Record Keeping and
```
Management on a Regenerative Farm (Order No. 29208065). Available from Publicly
```
```
Available Content Database. (2713561761).
```
```
http://ezproxy.taylors.edu.my/login?url=https://www.proquest.com/dissertations-these
```
s/building-spatial-database-agricultural-record/docview/2713561761/se-2
14. Kamati, W., Hashiyana, V., & Mutuku, J. (2024). Development of a near real-time
early warning agricultural system for disaster prediction. Malaysian Journal of
Computing and Applied Informatics.
```
https://ir.uitm.edu.my/id/eprint/61993/1/61993.pdf
```
15. Ramli, M.I., Ariffin, M.A.M., & Zainol, Z. (2023). Design of a Smart Portable
Farming Kit for Indoor Cultivation Using the Raspberry Pi Platform. Pertanika
```
Journal of Science & Technology, 31(4).
```
```
http://www.pertanika.upm.edu.my/resources/files/Pertanika%20PAPERS/JST%20Vol.
```
```
%2031%20(4)%20Jul.%202023/08%20JST-3789-2022.pdf
```
16. Zaki, N.S.M., Ramli, M.H.M., & Mohamed, Z. (2025). Prototype of an IoT-Based
Durian Tree Smart Switch Water and Soil Monitoring System. Journal of Applied
```
Engineering Design & Science, 2(1).PDF
```
17. Aydin, S., & Aydin, M.N. (2020). A Sustainable Multi-Layered Open Data Processing
Model for Agriculture: IoT-Based Case Study Using Semantic Web for Hazelnut
```
Fields. ASTES Journal, 5(2), 306–315.
```
```
https://www.astesj.com/v05/i02/p41/#1650442490543-5afe04f5-3111
```
18. Symeonaki, E., Arvanitis, K. G., & Piromalis, D. D. (2020). A context-aware
middleware cloud approach for integrating precision farming facilities into the IoT
```
toward agriculture 4.0. Applied Sciences, 10(3), 813.
```
```
https://doi.org/10.3390/app10030813
```
19. Cravero, A., Pardo, S., Galeas, P., & López Fenner, J. (2022). Data type and data
```
sources for agricultural big data and machine learning. Sustainability, 14(23), 16131.
```
```
https://doi.org/10.3390/su142316131
```
20. Olabanji, D. O. (2022). Towards the development of a decision framework for
portability in cloud-native architecture deployment.
```
https://www.researchgate.net/publication/383095362
```
21. Abgaz, Y., McCarren, A., Elger, P., Solan, D., & Lapuz, N. (2023). Decomposition of
monolith applications into microservices architectures: A systematic review. IEEE
Transactions on Cloud Computing. https://ieeexplore.ieee.org/document/10160171
22. Kamisetty, A., Narsina, D., & Rodriguez, M. (2023). Microservices vs. monoliths:
Comparative analysis for scalable software architecture design.
```
https://www.researchgate.net/publication/387645461
```
23. Trilles, S., González-Pérez, A., & Huerta, J. (2020). An IoT platform based on
```
microservices and serverless paradigms for smart farming purposes. Sensors, 20(8),
```
2418. https://doi.org/10.3390/s20082418
24. Padiya, S. D. (2023). Real-time crop prediction and fertilizer recommendation system
using machine learning and IoT [Undergraduate project report]. SSGMCE.
```
https://www.ssgmce.ac.in/uploads/UG_Projects/it/Gr%20No-12-Project-Report.pdf
```
120
25. Bhatt, R., Jindal, H., Chauhan, M., & Bhardwaj, V. (2024). Smart agriculture crop
disease detection using DL for enhanced crop health monitoring [PDF]. JUIT
Institutional Repository.
```
http://www.ir.juit.ac.in:8080/jspui/bitstream/123456789/11365/1/Smart%20Agricultur
```
e%20Crop%20Disease%20Detection%20using%20DL%20for%20Enhanced%20Cro
p%20Health%20Monitoring.pdf
26. Chan, J. J. (2024). Development of an IoT-integrated app for monitoring hydroponic
farming systems [Bachelor’s thesis, Universiti Tunku Abdul Rahman]. UTAR
Institutional Repository.
```
http://eprints.utar.edu.my/6825/1/2002845_CHAN_JIA_JUN.pdf
```
27. Koumandrakis, D. (2022). Artificial intelligence of things in agriculture: A web
application with smart irrigation [Master’s thesis, University of Macedonia].
```
https://dspace.lib.uom.gr/bitstream/2159/31806/1/KoumandrakisDimitriosMsc2022.p
```
df
28. Tomar, S., Aeron, V., & Ahmad, S. (2024). AgroBuddy: A tech-driven agricultural
```
management system. Kronika: A Research Journal, 10(2), 34–42.
```
```
https://kronika.ac/wp-content/uploads/39-KKJ2499.pdf
```
29. Kumar, A., Goyal, S., & Gandhi, A. B. (2021). Blockchain: A step towards innovation
in agriculture. In CEUR Workshop Proceedings, 3058, 722–728.
```
https://ceur-ws.org/Vol-3058/Paper-084.pdf
```
30. Ghimire, D. (2020). Comparative study on Python web frameworks: Flask and
Django. Theseus.
```
https://www.theseus.fi/bitstream/handle/10024/339796/Ghimire_Devndra.pdf
```
31. Rathnayake, L. R. (2024). Enhancing productivity in Sri Lanka’s agriculture sector
with a cloud-based system for data acquisition and representation to facilitate
informed decision-making. ResearchGate.
```
https://www.researchgate.net/publication/385311809
```
32. Aliche, S. K. C. (2024). Climate-smart IoT-based agriculture monitoring system.
Theseus. https://www.theseus.fi/bitstream/handle/10024/876070/Aliche_Kelvin.pdf
33. Biswas, B., Khan, R., & Thakare, Y. (2024). Enhancing weather prediction and
forecasting for agricultural applications using machine learning. In CRC Press eBooks
```
(pp. 506–511). https://doi.org/10.1201/9781003559085-88
```
34. Subramanian, A., Palanichamy, N., Ng, K.-W. ., & Aneja , S. (2025). Climate Change
Analysis in Malaysia Using Machine Learning . Journal of Informatics and Web
```
Engineering, 4(1), 307–319. https://doi.org/10.33093/jiwe.2025.4.1.22
```
35. Chong, N. S. C., Chong, L., & Chong, J. (2025). CITIC - Predictive Weather:
Harnessing machine learning for accurate forecasting. Journal of Advanced Research
```
in Applied Sciences and Engineering Technology, 63(1), 103–119.
```
```
https://doi.org/10.37934/araset.63.1.103119
```
36. Premachandra, J. S. A. N. W., & Kumara, P. P. N. V. (2021). A novel approach for
weather prediction for agriculture in Sri Lanka using Machine Learning techniques.
2021 International Research Conference on Smart Computing and Systems
```
Engineering (SCSE). https://doi.org/10.1109/scse53661.2021.9568319
```
121
37. Oshodi, I. (2022). Machine Learning-based Algorithms for Weather Forecasting.
Www.preprints.org. https://doi.org/10.20944/preprints202206.0428.v1
38. Kasinathan, T., Singaraju, D., & Uyyala, S. R. (2021). Insect classification and
detection in field crops using modern machine learning techniques. Information
```
Processing in Agriculture, 8(3), 446-457. https://doi.org/10.1016/j.inpa.2020.09.006
```
39. Karar, M. E., Alsunaydi, F., Albusaymi, S., & Alotaibi, S. (2021). A new mobile
application of agricultural pests recognition using deep learning in cloud computing
```
system. Alexandria Engineering Journal, 60(5), 4423–4432.
```
```
https://doi.org/10.1016/j.aej.2021.03.009
```
40. Eray Önler (2021). REAL TIME PEST DETECTION USING YOLOv5.
```
International Journal of Agricultural and Natural Sciences, 14(3), pp.232–246.
```
```
https://www.ijans.org/index.php/ijans/article/view/550
```
41. Maican, E., Iosif, A. and Maican, S. (2023). Precision Corn Pest Detection: Two-Step
```
Transfer Learning for Beetles (Coleoptera) with MobileNet-SSD. Agriculture, 13(12),
```
pp.2287–2287. doi:https://doi.org/10.3390/agriculture13122287.
42. Yang, S., Xing, Z., Wang, H., Dong, X., Gao, X., Liu, Z., Zhang, X., Li, S., & Zhao,
Y. (2023). Maize-YOLO: A New High-Precision and Real-Time Method for Maize
```
Pest Detection. Insects, 14(3), 278. https://doi.org/10.3390/insects14030278
```
43. Ibrahim, U., & Danmaigoro, A. (2024). Human-Computer Interaction in Agricultural
```
User Interfaces. International Journal of Applied and Scientific Research, 2(2),
```
187–198. https://doi.org/10.59890/ijasr.v2i2.1381
44. Setiyawati, N., Dwi Purnomo, H., & Mailoa, E. (2022). User Experience Design on
Visualization of Mobile-Based Land Monitoring System Using a User-Centered
```
Design Approach. International Journal of Interactive Mobile Technologies (IJIM),
```
```
16(03), 47–65. https://doi.org/10.3991/ijim.v16i03.28499
```
45. Osman, M. J., Idris, N. H., Majid, Z., & Mohd Salleh, M. R. (2022). MOBILE USER
INTERFACE DESIGN FOR SMALLHOLDER AGRICULTURE TO BE A SMART
```
FARMER: A SCOPING REVIEW. Journal of Information System and Technology
```
```
Management, 7(25), 92–101. https://doi.org/10.35631/jistm.725007
```
46. Leng, K. Y. (2023). Farm management information system (Crop planning and
```
tracking modules) - UTAR Institutional Repository. Utar.edu.my.
```
```
http://eprints.utar.edu.my/5788/1/fyp_CS_2023_LKY.pdf
```
47. Sharjeel Moqrab Khan, Aftab Ul Nabi, & Tahir Hussain Bhanbhro. (2022).
```
Comparative Analysis between Flutter and React Native. 1(1), 15–28.
```
```
https://doi.org/10.58921/ijaims.v1i1.19
```
48. Stender, S., & Åkesson, H. (2020). Cross-platform Framework Comparison : Flutter
& React Native. DIVA.
```
https://www.diva-portal.org/smash/record.jsf?pid=diva2%3A1440825&dswid=1954
```
49. Dart. (n.d.). Dart overview. Dart.dev. https://dart.dev/overview
50. GeeksforGeeks. (2020, July 10). Comparison of Dart and JavaScript. GeeksforGeeks.
```
https://www.geeksforgeeks.org/comparison-of-dart-and-javascript/
```
51. Protect your crops. Harvest more! (n.d.). Agrio. https://agrio.app/
52. Ministry of Economy. (2025, February 28). The Malaysian Economy in Figures 2024.
ekonomi.gov.my. https://ekonomi.gov.my/sites/default/files/2025-04/MEIF_2024.pdf
122
53. United Nations. (n.d.). World population projected to reach 9.8 billion in 2050, and
11.2 billion in 2100 | United Nations.
```
https://www.un.org/en/desa/world-population-projected-reach-98-billion-2050-and-11
```
2-billion-2100
54. Robinson, L. (2025, April 3). Top challenges for modern agriculture in 2024.
Verdesian Life Sciences. https://vlsci.com/blog/top-issues-in-agriculture-2024/
55. Li, K., Jin, Y., & Zhou, J. (2023). Are vulnerable farmers more easily influenced?
Heterogeneous effects of Internet use on the adoption of integrated pest management.
```
Journal of Integrative Agriculture, 22(10), 3220–3233.
```
```
https://doi.org/10.1016/j.jia.2023.08.005
```
56. File, D. J. M., & Nhamo, G. (2023). Farmers’ choice for indigenous practices and
```
implications for climate-smart agriculture in northern Ghana. Heliyon, 9(11), e22162.
```
```
https://doi.org/10.1016/j.heliyon.2023.e22162
```
57. Rajak, P., Ganguly, A., Adhikary, S., & Bhattacharya, S. (2023). Internet of Things
and smart sensors in agriculture: Scopes and challenges. Journal of Agriculture and
Food Research, 14, 100776. https://doi.org/10.1016/j.jafr.2023.100776
58. Bridging the IoT gap: The challenges and potential of Malaysia’s tech landscape.
```
(2023, August 7). IoT World.
```
```
https://iotworld.co/2023/08/bridging-the-iot-gap-the-challenges-and-potential-of-mala
```
ysias-tech-landscape/
59. Mazlan Abbas, Dr. (2023, March 8). The state of IoT adoption in Malaysia:
opportunities and obstacles.
```
https://www.linkedin.com/pulse/state-iot-adoption-malaysia-opportunities-obstacles-d
```
r-mazlan-abbas/
60. Larger population, larger people: humanity will require 80% more food by 2100.
```
(2019, December 11). Population Matters.
```
```
https://populationmatters.org/news/2019/12/larger-population-larger-people-humanity
```
-will-require-80-more-food-by-2100/
61. Duguma, A. L., & Bai, X. (2024). How the internet of things technology improves
```
agricultural efficiency. Artificial Intelligence Review, 58(2).
```
```
https://doi.org/10.1007/s10462-024-11046-0
```
62. IoT Environmental Monitoring Sensors. (n.d.).
```
https://www.niubol.com/Product-knowledge/IoT-Environmental-Monitoring-Sensors.
```
html
63. Glória, A., Cardoso, J., & Sebastião, P. (2021). Sustainable irrigation system for
```
farming supported by machine learning and Real-Time sensor data. Sensors, 21(9),
```
3079. https://doi.org/10.3390/s21093079
64. Dong, Y., Werling, B., Cao, Z., & Li, G. (2024). Implementation of an in-field IoT
system for precision irrigation management. Frontiers in Water, 6.
```
https://doi.org/10.3389/frwa.2024.1353597
```
65. Alfred, R., Obit, J. H., Chin, C. P., Haviluddin, H., & Lim, Y. (2021). Towards Paddy
Rice Smart Farming: A review on big data, machine learning, and rice production
tasks. IEEE Access, 9, 50358–50380. https://doi.org/10.1109/access.2021.3069449
123
66. Rodríguez, J. P., Montoya-Munoz, A. I., Rodriguez-Pabon, C., Hoyos, J., & Corrales,
J. C. (2021). IoT-Agro: A smart farming system to Colombian coffee farms.
Computers and Electronics in Agriculture, 190, 106442.
```
https://doi.org/10.1016/j.compag.2021.106442
```
67. Siddiquee, K. N., Islam, M. S., Singh, N., Gunjan, V. K., Yong, W. H., Huda, M. N.,
```
& Naik, D. S. B. (2022). Development of algorithms for an IoT-Based smart
```
agriculture monitoring system. Wireless Communications and Mobile Computing,
2022, 1–16. https://doi.org/10.1155/2022/7372053
68. Amr, M. E., Al-Awamry, A. A., Elmenyawi, M. A., & Tag Eldien, A. S. (2022).
Design and implementation of a low-cost IoT node for data processing, case study:
```
Smart agriculture. Journal of Communications, 17(2), 99–109.
```
```
https://doi.org/10.12720/jcm.17.2.99-109
```
69. Kumar, V., Sharma, K. V., Kedam, N., Patel, A., Kate, T. R., & Rathnayake, U.
```
(2024). A comprehensive review on smart and sustainable agriculture using IoT
```
technologies. Smart Agricultural Technology, 8, 100487.
```
https://doi.org/10.1016/j.atech.2024.100487
```
70. Morchid, A., Alami, R. E., Raezah, A. A., & Sabbar, Y. (2023). Applications of
```
internet of things (IoT) and sensors technology to increase food security and
```
agricultural Sustainability: Benefits and challenges. Ain Shams Engineering Journal,
```
15(3), 102509. https://doi.org/10.1016/j.asej.2023.102509
```
71. De Araujo Zanella, A. R., Da Silva, E., & Albini, L. C. P. (2020). Security challenges
to smart agriculture: Current state, key issues, and future directions. Array, 8, 100048.
```
https://doi.org/10.1016/j.array.2020.100048
```
72. Nawaz, M., & Babar, M. I. K. (2025). IoT and AI for smart agriculture in
resource-constrained environments: challenges, opportunities and solutions. Discover
```
Internet of Things, 5(1). https://doi.org/10.1007/s43926-025-00119-3
```
73. Tang, P., Liang, Q., Li, H., & Pang, Y. (2024). Application of Internet-of-Things
Wireless Communication Technology in Agricultural irrigation Management: A
```
review. Sustainability, 16(9), 3575. https://doi.org/10.3390/su16093575
```
74. Kim, W., Lee, W., & Kim, Y. (2020). A review of the applications of the internet of
```
things (IoT) for agricultural automation. Journal of Biosystems Engineering, 45(4),
```
385–400. https://doi.org/10.1007/s42853-020-00078-3
75. Mishra, A., Alzoubi, Y. I., & Gavrilovic, N. (2024). Quality attributes of software
architecture in IoT-based agricultural systems. Smart Agricultural Technology, 8,
100523. https://doi.org/10.1016/j.atech.2024.100523
76. Kour, V. P., & Arora, S. (2020). Recent developments of the internet of things in
```
agriculture: a survey. IEEE Access, 8, 129924–129957.
```
```
https://doi.org/10.1109/access.2020.3009298
```
77. Chamara, N., Islam, M. D., Bai, G., Shi, Y., & Ge, Y. (2022). Ag-IoT for crop and
environment monitoring: Past, present, and future. Agricultural Systems, 203, 103497.
```
https://doi.org/10.1016/j.agsy.2022.103497
```
78. Mansoor, S., Iqbal, S., Popescu, S. M., Kim, S. L., Chung, Y. S., & Baek, J. (2025).
Integration of smart sensors and IOT in precision agriculture: trends, challenges and
124
future prospectives. Frontiers in Plant Science, 16.
```
https://doi.org/10.3389/fpls.2025.1587869
```
79. De Los Ángeles Calva Jiménez, A., De Almeida, C. D. G. C., Júnior, J. a. S., De
```
Morais, J. E. F., De Almeida, B. G., & De Andrade, F. H. N. (2019). Accuracy of
```
capacitive sensors for estimating soil moisture in northeastern Brazil. Soil and Tillage
Research, 195, 104413. https://doi.org/10.1016/j.still.2019.104413
80. Romavh, G. (2025, March 3). What’s the difference between PT100 and DS18B20
sensors? ANDIVI.
```
https://www.andivi.com/whats-the-difference-between-pt100-and-ds18b20-sensors/
```
81. Santos, R., & Santos, R. (2019, July 26). DHT11 vs DHT22 vs LM35 vs DS18B20 vs
BME280 vs BMP180 | Random Nerd Tutorials. Random Nerd Tutorials.
```
https://randomnerdtutorials.com/dht11-vs-dht22-vs-lm35-vs-ds18b20-vs-bme280-vs-b
```
mp180/
82. Instructables. (2017, October 20). BH1750 Digital Light Sensor. Instructables.
```
https://www.instructables.com/BH1750-Digital-Light-Sensor/
```
83. AS7341 Spectral Color Sensor - Waveshare Wiki. (n.d.).
```
https://www.waveshare.com/wiki/AS7341_Spectral_Color_Sensor
```
84. LI-COR LI-200R Pyranometer, Bare Leads LI-200R | Onset’s HOBO Data Loggers.
```
(n.d.).
```
```
https://www.onsetcomp.com/products/sensors/li-200r?srsltid=AfmBOorKzPH8SIsgO
```
xxm2z-_50XFw3wVap7xCPrMPRYosVXuatDNK4Bx
85. SP-110-L - Apogee Silicon Pyranometer. (n.d.). https://www.campbellsci.asia/sp-110
86. Oliynyk, K. (2025, April 30). Arduino vs Raspberry PI: Key Differences &
Comparison Table. webbylab.
```
https://webbylab.com/blog/arduino-vs-raspberry-pi-comparison/
```
87. What is better, the Arduino Uno or the ESP32? (2024, January 25). BotShop.
```
https://www.botshop.co.za/blog/projects-6/what-is-better-the-arduino-uno-or-the-esp3
```
2-36
88. OpenELAB. (2024, October 16). ESP32 vs Arduino vs Raspberry Pi Pico: Which is
Better? OpenELAB Technology Ltd.
```
https://openelab.io/blogs/learn/esp32-vs-arduino-vs-raspberry-pi-pico-which-is-better
```
?srsltid=AfmBOormqUEbjvIl1047ojiGOKGBHbZkYRnjunooF-HlQhcFYv1jjCir
89. Wokwi - - — Arduino ESP32 latest documentation. (n.d.).
```
https://docs.espressif.com/projects/arduino-esp32/en/latest/third_party/wokwi.html
```
90. Welcome to Wokwi! | Wokwi Docs. (n.d.). https://docs.wokwi.com/#why-wokwi
91. Mousavi, S. K., Ghaffari, A., Besharat, S., & Afshari, H. (2021). Security of internet
```
of things based on cryptographic algorithms: a survey. Wireless Networks, 27(2),
```
1515–1555. https://doi.org/10.1007/s11276-020-02535-5
92. Gomstyn, A., & Jonker, A. (2025b, April 16). What is smart farming?. IBM.
```
https://www.ibm.com/think/topics/smart-farming#:~:text=Smart%20farming%2C%20
```
also%20known%20as,to%20the%20International%20Monetary%20Fund.&text=Clim
ate%20change%20is%20making%20it,promote%20resilience%20in%20agricultural
%20production.%E2%80%9D
125
93. Nangalia, Ms. P. (2024, December 9). Israel’s Drone Technology: Applications in
Defense, Agriculture, and Beyond. India - Israel Trade & Economic Office, Embassy
of Israel.
```
https://itrade.gov.il/india/2024/12/09/israels-drone-technology-applications-in-defense
```
-agriculture-and-beyond/
94. Karunathilake, E. M. B. M., Le, A. T., Heo, S., Chung, Y. S., & Mansoor, S. (2023).
The Path to Smart Farming: Innovations and Opportunities in Precision Agriculture.
```
Agriculture, 13(8), 1593. https://doi.org/10.3390/agriculture13081593
```
95. Becker, S. (2024, April 4). US farms are making an urgent push into AI. It could help
feed the world.
```
https://www.bbc.com/worklife/article/20240325-artificial-intelligence-ai-us-agricultur
```
e-farming
96. Padrón, R. S., Feyen, J., Córdova, M., Crespo, P., & Célleri, R. (2020). Comparación
entre Pluviómetros Cuantifica Deficiencias en el Monitoreo de la Precipitación. La
```
Granja, 31(1), 7–20. https://doi.org/10.17163/lgr.n31.2020.0
```
97. Subburaj, S. D. R., Eswaramoorthy, C., Latha, V. G., & Chinnasamy, R. K. P. (2025,
```
January 1). Efficient pest detection through Advanced Machine Learning Technique –
```
Current Agriculture Research Journal.
```
https://www.agriculturejournal.org/volume12number3/efficient-pest-detection-throug
```
h-advanced-machine-learning-technique/
98. Whittaker, A. (2021, September 18). Save orchards from pests with Raspberry Pi.
Raspberry Pi.
```
https://www.raspberrypi.com/news/save-orchards-from-pests-with-raspberry-pi/
```
99. Olsson, E. (2022, November). Detection of pests in agriculture using machine
learning. DiVA Portal.
```
https://www.diva-portal.org/smash/get/diva2:1947258/FULLTEXT01.pdf
```
100. Mustofa, A. A., Dagnew, Y. A., Gantela, P., & Idrisi, M. J. (2023). SECHA: a
smart Energy-Efficient and Cost-Effective home automation system for developing
countries. Journal of Computer Networks and Communications, 2023, 1–12.
```
https://doi.org/10.1155/2023/8571506
```
101. Mathe, S. E., Kondaveeti, H. K., Vappangi, S., Vanambathina, S. D., &
```
Kumaravelu, N. K. (2024). A comprehensive review on applications of Raspberry Pi.
```
Computer Science Review, 52, 100636. https://doi.org/10.1016/j.cosrev.2024.100636
102. El-Khozondar, H. J., Mtair, S. Y., Qoffa, K. O., Qasem, O. I., Munyarawi, A. H.,
```
Nassar, Y. F., Bayoumi, E. H., & Halim, A. a. E. B. a. E. (2024). A smart energy
```
monitoring system using ESP32 microcontroller. e-Prime - Advances in Electrical
Engineering Electronics and Energy, 9, 100666.
```
https://doi.org/10.1016/j.prime.2024.100666
```
126