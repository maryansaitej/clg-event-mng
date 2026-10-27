from pathlib import Path
import json,re,math,html
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_JUSTIFY,TA_CENTER
from reportlab.lib import colors
from reportlab.platypus import Paragraph,Table,TableStyle,Spacer,Image,Flowable
from pypdf import PdfReader,PdfWriter
from pypdf.generic import ContentStream,NameObject
R=Path(__file__).resolve().parents[3];D=R/'tmp/pdfs/revision';A=D/'assets';OUT=R/'output/pdf/College_Event_Management_Report_Corrected_20_Pages.pdf'
for n,s in [('TNR',''),('TNRB',' Bold'),('TNRI',' Italic')]:pdfmetrics.registerFont(TTFont(n,'/System/Library/Fonts/Supplemental/Times New Roman'+s+'.ttf'))
pdfmetrics.registerFontFamily('TNR',normal='TNR',bold='TNRB',italic='TNRI',boldItalic='TNRB')
S={
'p':ParagraphStyle('p',fontName='TNR',fontSize=12,leading=17,alignment=TA_JUSTIFY,spaceAfter=10),
'h':ParagraphStyle('h',fontName='TNRB',fontSize=15,leading=19,spaceBefore=8,spaceAfter=10),
'center':ParagraphStyle('center',fontName='TNR',fontSize=12,leading=17,alignment=TA_CENTER,spaceAfter=8),
'coverhead':ParagraphStyle('coverhead',fontName='TNRB',fontSize=15,leading=20,alignment=TA_CENTER,spaceAfter=10),
'cap':ParagraphStyle('cap',fontName='TNRI',fontSize=12,leading=16,alignment=TA_CENTER,spaceBefore=6,spaceAfter=12),
'cell':ParagraphStyle('cell',fontName='TNR',fontSize=12,leading=15),
}
pages={i:[] for i in range(1,21)};pg=1;headings=[];figures=[];tables=[]
def page(n):
 global pg;pg=n

def p(t,style='p'):pages[pg].append(Paragraph(t,S[style]))
def h(t,toc=True):
 p(t,'h')
 if toc:headings.append((t,pg))
def gap(n):pages[pg].append(Spacer(1,n))
def img(n,w,hh):pages[pg].append(Image(str(A/n),width=w,height=hh))
def bullet(t):p('&#8226; '+t)
def tab(headers,rows,widths):
 data=[[Paragraph('<b>'+html.escape(x)+'</b>',S['cell']) for x in headers]]+[[Paragraph(html.escape(x),S['cell']) for x in row] for row in rows]
 t=Table(data,colWidths=widths,hAlign='LEFT');t.setStyle(TableStyle([('GRID',(0,0),(-1,-1),.5,colors.HexColor('#777777')),('BACKGROUND',(0,0),(-1,0),colors.HexColor('#eeeeee')),('BACKGROUND',(0,1),(-1,-1),colors.white),('VALIGN',(0,0),(-1,-1),'TOP'),('LEFTPADDING',(0,0),(-1,-1),7),('RIGHTPADDING',(0,0),(-1,-1),7),('TOPPADDING',(0,0),(-1,-1),7),('BOTTOMPADDING',(0,0),(-1,-1),7)]));pages[pg].append(t)
class Diagram(Flowable):
 def __init__(self,kind,height):super().__init__();self.kind=kind;self.width=468;self.height=height
 def draw(self):
  c=self.canv;c.saveState();c.setFillColor(colors.white);c.rect(0,0,468,self.height,fill=1,stroke=0);c.setLineWidth(.8)
  def text(x,y,t,b=False):
   c.setFillColor(colors.black);c.setFont('TNRB' if b else 'TNR',12)
   for i,s in enumerate(t.split('\n')):c.drawCentredString(x,y-i*16,s)
  def box(x,y,w,hh,t):
   c.setStrokeColor(colors.HexColor('#555555'));c.setFillColor(colors.HexColor('#f5f5f5'));c.rect(x,y,w,hh,fill=1,stroke=1);text(x+w/2,y+hh/2+(t.count('\n')*8)-4,t,True)
  def arrow(x1,y1,x2,y2):
   c.setStrokeColor(colors.HexColor('#555555'));c.line(x1,y1,x2,y2);a=math.atan2(y2-y1,x2-x1)
   for b in [-.45,.45]:c.line(x2,y2,x2-6*math.cos(a+b),y2-6*math.sin(a+b))
  if self.kind=='usecase':
   c.rect(93,8,369,338);text(277,325,'College Event Management Website',True)
   for yy,who,cases in [(260,'Student',['Register / sign in','Browse and join clubs','Register / pay / view bookings']),(157,'Club',['Manage club profile','Create and publish events','Manage registrations']),(54,'Admin',['Review users','Approve or reject clubs','Moderate events'])]:
    c.circle(37,yy+18,6);c.line(37,yy+12,37,yy-8);c.line(25,yy+3,49,yy+3);c.line(37,yy-8,27,yy-20);c.line(37,yy-8,47,yy-20);text(37,yy-38,who,True)
    for j,st in enumerate(cases):
     y=yy+28-j*29;c.setFillColor(colors.HexColor('#f8f8f8'));c.ellipse(171,y-13,446,y+13,fill=1);text(309,y-4,st);c.line(49,yy+3,171,y)
  if self.kind=='concept':
   box(90,288,288,44,'Student, club and administrator input');arrow(234,288,234,267)
   box(90,219,288,48,'Identity, validation and\npermission checks');arrow(234,219,234,195)
   for x,t in [(0,'Clubs and\nmemberships'),(160,'Events and\nregistrations'),(320,'Payments and\nadministration')]:box(x,139,148,54,t)
   c.line(74,139,74,118);c.line(394,139,394,118);c.line(74,118,394,118);c.line(234,139,234,118);arrow(234,118,234,95)
   box(90,47,288,48,'PostgreSQL: shared records');arrow(234,47,234,25);text(234,7,'Dashboards, confirmations and registration history')
  if self.kind=='architecture':
   for y,title,detail in [(288,'Presentation layer','React + TypeScript + Vite + Tailwind CSS'),(211,'Security and API boundary','Session authentication and protected JSON APIs'),(126,'Application layer','Java + Spring Boot + Spring Security'),(41,'Persistence layer','Spring Data JPA + PostgreSQL / Supabase')]:
    box(14,y,440,56,title+'\n'+detail)
   for a,b in [(288,267),(211,182),(126,97)]:arrow(234,a,234,b)
   text(234,12,'The browser displays information; the backend enforces rules.')
  c.restoreState()
def figure(kind,title,height):
 pages[pg].append(Diagram(kind,height));num=len(figures)+1;figures.append((f'Figure {num}. {title}',pg));p(f'Figure {num}. {title}','cap')
# Retain the academic cover layout and institutional details; apply the specified type sizes.
page(1);p('Web Programming Course End Project Report On','center');gap(10)
p('College Event Management Website','coverhead');gap(10);p('in','center');p('COMPUTER SCIENCE AND ENGINEERING','coverhead');p('(IoT with Cyber Security Including Blockchain Technology)','center');gap(6);p('by','center');gap(20)
p('Names with<br/>Roll numbers','center');gap(22);p('Under the Supervision of','center');p('<b>N. Sujata Gupta</b>','center');p('Assistant Professor','center');p('Department of Computer Engineering and Technology','center');gap(12);img('crest.png',62,82);gap(17)
p('Department of Computer Engineering and Technology','center');p('Chaitanya Bharathi Institute of Technology','coverhead');p('(Autonomous)','center')
page(2);p('(Affiliated to Osmania University, Hyderabad)','center');p('Hyderabad, TELANGANA (INDIA) - 500 075','center');p('[2025-2026]','center');gap(28);img('banner.png',452,84);gap(28);p('CERTIFICATE','coverhead')
p('This is to certify that the Course End Project titled <b>"College Event Management Website"</b> is a bonafide work carried out by the students named on the title page, of the Department of Computer Engineering and Technology, Chaitanya Bharathi Institute of Technology, Hyderabad, Telangana (India), submitted in partial fulfilment of the requirements for the award of the degree of Bachelor of Engineering in the academic year 2025-2026.')
gap(42);h('Coordinators',False);p('Ms. N. Sujata Gupta<br/>Assistant Professor, Department of CET, CBIT');gap(32)
t=Table([[Paragraph('Place: Hyderabad, Telangana<br/>Date: __________________',S['p']),Paragraph('<b>Head of the Department</b><br/>Professor, CET Department, CBIT',S['p'])]],colWidths=[242,226]);t.setStyle(TableStyle([('VALIGN',(0,0),(-1,-1),'TOP'),('LEFTPADDING',(0,0),(-1,-1),0)]));pages[pg].append(t)
page(7);h('Abstract')
p('College events are often announced through notices, messages and separate registration forms. This arrangement makes it difficult for students to identify relevant activities and for organizers to maintain consistent participant and fee records. The College Event Management Website, implemented as Campus Commons, brings these activities into a common platform for students, clubs and administrators.')
p('Students can create an account, maintain a profile, browse clubs and events, join clubs, register for activities and review their registrations. Clubs maintain organizational profiles and create events with specified dates, venues, fees, capacities and eligibility conditions. Administrators review club applications, inspect user records and moderate events. Each role receives an interface suited to its responsibilities.')
p('The frontend uses React, TypeScript, Vite and Tailwind CSS. A Java Spring Boot backend provides application services, applies Spring Security access controls and manages records through Spring Data JPA. PostgreSQL is the main database, with Supabase PostgreSQL available as a compatible hosting option. The frontend presents information and collects input, while the backend validates requests and maintains the shared records.')
p('The platform supports both free and fee-based events. Free registrations are confirmed directly. The current fee-payment facility is a development simulator that demonstrates payment status and cancellation behaviour without collecting real money. Public event information is separated from personal records and administrative controls.')
p('This report reviews the project background, problem statement, relevant approaches and proposed model. It explains the principal components, conceptual framework, architecture and source organization at an overview level. The result is a coordinated design for college event administration that gives students clear access to activities and gives organizers a common place to manage participation.')
p('<b>Keywords:</b> college event management, clubs, React, Java, Spring Boot, PostgreSQL.')
page(8);h('1. Introduction')
p('A college event involves more than publishing a title and date. The organizer must communicate eligibility, reserve a venue, control participation and account for registration fees. Students need an accurate description of the activity and a reliable indication that their booking has been accepted. The proposed website connects these responsibilities through a shared record of clubs, events and registrations.')
h('1.1 Background')
p('Campus activities include technical workshops, cultural programmes, sports meetings and student-club sessions. Their administration commonly involves a mixture of announcements, forms and spreadsheets. When the same event is represented in several places, a revised deadline or venue may not reach every participant. A centralized website can make the published event record the reference point for students and organizers.')
p('The project uses a browser interface backed by a Java application service. Public information remains easy to discover, while personal registrations and organizer controls require authentication. The database stores durable records so that a page refresh or a change of browser does not remove a student\'s booking history.')
h('1.2 Motivation')
p('The primary motivation is to reduce manual coordination while preserving clear accountability. Students should be able to distinguish an available event from a full or closed event before attempting registration. Clubs should be able to publish complete information and review participants without maintaining duplicate lists. Administrators need a way to review organizations and respond to inappropriate or cancelled events.')
p('The project also demonstrates how a responsive frontend can work with a structured backend. Clear forms make the system approachable, while common records and server-side checks make its results dependable. Both aspects are needed for a practical college platform.')
page(9);h('1.3 Project Scope')
p('The scope covers one college and three roles: student, club and administrator. It includes account access, club membership, event publication, registration and a simulated fee-payment facility. Event eligibility is evaluated against the department and study year entered in a student profile.')
bullet('<b>Students:</b> register or log in, browse clubs and events, join clubs, register for events, complete the available fee step and view registration history.')
bullet('<b>Clubs:</b> register or log in, maintain a profile, create and edit events, publish approved activities and manage student registrations.')
bullet('<b>Administrators:</b> review users and clubs, approve or reject club applications, and moderate event publication.')
p('The scope is limited to the basic functions described above. Live financial settlement and institutional identity verification are outside the current implemented scope.')
h('1.4 Technologies Used')
p('<b>React and TypeScript</b> implement reusable pages, typed information models and interactive forms. <b>Vite</b> supports frontend development and building the browser application. <b>Tailwind CSS</b> provides styling utilities for consistent, responsive layouts.')
p('<b>Java and Spring Boot</b> provide the backend runtime and application structure. <b>Spring Security</b> controls authentication and protected operations. <b>Spring Data JPA</b> connects the application model to the database and supports record retrieval and updates.')
p('<b>PostgreSQL</b> stores accounts, clubs, events, memberships and registrations. <b>Supabase PostgreSQL</b> is a compatible managed database option. In either arrangement, the Java backend remains responsible for application rules and access control.')
page(10);h('2. Problem Statement')
p('The problem is to provide a consistent event-management process in which published information, eligibility, remaining capacity and payment status agree across all user interfaces. The system must prevent unauthorized changes, duplicate registrations and acceptance of bookings after an event becomes unavailable.')
p('A student should be able to identify the organizer, understand participation conditions and determine whether a registration is confirmed. An organizer should be able to manage an event without collecting the same details through several channels. Administrative review should operate on the same club and event records used by the rest of the platform.')
h('2.1 Limitations of Existing Systems')
p('A workflow based on separate notices, forms and payment references requires organizers to reconcile records manually. Capacity may be checked only after submissions arrive, and students may be uncertain whether submitting a form confirms a seat. General-purpose tools can support individual tasks, but college-specific approval and eligibility rules require additional coordination.')
p('Fragmented records also make changes harder to communicate. A date may be updated in an announcement while an older form remains accessible. Participant lists can contain repeated entries, and fee information may need to be matched manually with the corresponding student.')
h('2.2 Need for an Integrated Event and Club Platform')
p('A shared platform connects an approved club to its published activities and links each student to a registration record. Schedule, fee and venue information is presented through the same event page. Organizers receive participant records from the booking system, reducing the need to copy data between unrelated tools.')
p('Integration also clarifies responsibility. Clubs prepare and manage their activities, students maintain their own participation records, and administrators review organizations and moderate events. The website supports these responsibilities within one coordinated interface.')
page(11);h('2.3 Importance of Data Privacy and User Experience')
p('Student names, contact details, college identifiers and booking histories should be disclosed only to authorized users. Authentication alone is insufficient: the backend must also verify whether a club owns an event or a student owns a registration before allowing access to it.')
p('The interface must explain validation errors, payment status and cancellation outcomes in language that students can act upon. Labelled fields, visible focus, readable status text and consistent navigation help users complete tasks with fewer misunderstandings. Private account details do not belong in public event listings.')
h('2.4 Lack of Personalization and Adaptability')
p('A single undifferentiated event list can obscure relevant opportunities. The website provides category, date and fee filters, club membership and a student dashboard of upcoming commitments. Department and year rules tailor eligibility to the selected event.')
p('These features use explicit preferences and stated participation rules. Students can choose relevant activities without depending on automated predictions. The current application does not infer interests through machine learning or alter eligibility based on browsing behaviour.')
h('2.5 Integration and Scalability Issues')
p('Payment services and college identity systems introduce external dependencies. The project keeps payment behaviour behind a separate provider interface and retains application rules in the Java backend. This makes the boundary between the website and an external service clear.')
p('Organized modules, bounded result lists and suitable database queries help the platform handle growing records. The present design is intended for a single college and a single backend instance. Wider operation would require further infrastructure and evaluation, rather than being assumed from the architecture alone.')
page(12);h('2.6 Use Case Overview')
p('Students discover and register for activities; clubs prepare and operate them; administrators approve organizations and moderate publication. Public browsing is available before login. Actions that change records require the appropriate authenticated role. Figure 1 summarizes these responsibilities.')
figure('usecase','UML use case overview',355)
h('Example Use Case Scenario',False)
p('A second-year student selects a workshop and reviews its fee, date, venue and eligibility. The backend checks the profile and available capacity before creating a registration. A free event is confirmed directly; a fee-based event proceeds to the available simulated payment step. The student can review the resulting status in the registration workspace.')
p('The organizing club sees the same registration in its participant list. An administrator can review the club\'s approval status and moderate the event when necessary. The scenario connects discovery, participation and administration without separate lists.')
page(13);h('3. Literature Review')
p('This review examines approaches relevant to event administration and the technical concepts used by the project. It compares workflow capabilities rather than ranking commercial products. The review supports the choice of an integrated website with a separate frontend, backend and database.')
h('3.1 Evolution of Digital Event Management Systems')
p('Online forms simplify collection, but a form alone does not inherently enforce event capacity or publication authority. Component-based interfaces and application services allow discovery, booking and management to use shared records. The React interface follows this component-based approach.')
h('3.2 Adaptive and Personalized Event Management Models')
p('Selected categories, joined clubs and upcoming registrations provide a transparent form of personalization. These explicit choices make relevant activities easier to locate. The project adopts this approach because its results can be understood and controlled by users.')
h('3.3 Data Visualization and Insight Generation Systems')
p('Event cards summarize schedule, venue, fee and availability. Workspaces place registration status and participant information near the actions that use them. This presentation helps students and clubs interpret records without reading raw database values. Detailed attendance analytics are not included in this basic model.')
h('3.4 Integration of Security Features in Digital Applications')
p('Access control should be applied to both the user\'s role and the particular record being requested. Spring Security supports the authentication boundary, while backend services check ownership and participation rules. These responsibilities complement the frontend: hiding a button alone does not protect the underlying operation.')
p('The selected approach therefore combines an understandable interface with controlled access to shared records. Account security, appropriate disclosure and clear feedback remain part of normal application behaviour rather than separate user tasks.')
page(14);h('3.5 Comparison to Existing Tools')
p('Table 1 compares common organizational approaches with the proposed website. The entries describe how work is coordinated; they do not represent measured rankings of commercial products.')
tables.append(('Table 1. Comparison of event-management approaches',pg));p(tables[-1][0],'cap')
tab(['Feature / Aspect','Forms and Sheets','Separate Tools','Proposed Website'],[
 ['Event discovery','Separate notices','Separate catalog','Shared catalog'],['Club approval','Manual review','Separate review','Admin approval'],['Capacity control','Manual counting','Cross-tool checks','Backend checks'],['Fee status','Manual matching','Separate record','Linked demo status'],['Data presentation','Spreadsheet rows','Separate reports','Event and booking views'],['Personalization','Manual selection','Separate preferences','Filters and memberships'],['Data privacy','File permissions','Separate accounts','Role-based access'],['Unified platform','Manual coordination','Multiple interfaces','Connected workspaces']],[112,110,118,128])
gap(12);h('3.6 Research Gaps')
p('The main gap is between collecting registrations and maintaining a dependable process. Independent notices and forms do not automatically connect club approval, event availability, participant records and fee status.')
bullet('A shared and current source of event information is needed.')
bullet('Publication and registration must follow consistent rules.')
bullet('Personal records need restricted access and clear status feedback.')
p('These are design requirements identified through workflow analysis. They support the proposed model without claiming a campus-wide user study or measured participation improvement.')
page(15);h('3.7 Conceptual Framework Model')
p('The conceptual framework connects user input to identity checks, domain operations and shared records. Each operation produces a response suited to the requesting role. Club membership, event registration and payment status remain separate concepts so that joining a club does not automatically register a student for its events.')
figure('concept','Conceptual framework model',338)
h('Key Framework Features',False)
p('<b>Modularity:</b> account access, clubs, events and registrations have distinct responsibilities. <b>Shared records:</b> the database provides a consistent basis for views across the platform. <b>User-centred interaction:</b> forms and status messages support the main student and organizer tasks.')
p('<b>Controlled access:</b> the backend authorizes changes before saving them. <b>Maintainability:</b> the interface and external payment integration can be changed without transferring authority over event fees or capacity to the browser.')
page(16);h('4. Proposed Model')
p('The proposed model is a three-tier web application with public discovery and authenticated workspaces. A React single-page application communicates with a Java Spring Boot backend through JSON APIs. PostgreSQL holds the shared records. The design separates user interaction from application rules and storage.')
p('This separation gives each layer a clear responsibility. The frontend organizes pages and collects input. The backend validates requests, identifies the permitted operation and returns the result. The database retains records needed by students, clubs and administrators.')
h('4.1 System Overview')
p('Students, clubs and administrators share the same catalog but receive different controls. A new club begins in a pending state and requires approval before publication. Published events accept registrations only when participation conditions are met and capacity remains available.')
p('Students use event pages to inspect schedule, venue, fee and eligibility details. Their workspace presents joined clubs and registration history. Clubs use their workspace to maintain a profile, prepare activities and inspect participant records for their own events.')
p('Administrators review clubs, inspect user records and moderate events. Approval affects which organizers can publish, while moderation affects public event visibility. These decisions operate on the same records used by the other workspaces.')
p('The current payment facility demonstrates fee-related states without collecting real money. This boundary is visible in the development application. The overview therefore distinguishes the implemented registration functions from live financial settlement.')
p('The model is intended to make event administration coherent and understandable. It combines a responsive browser interface with a Java service and a relational database, while keeping the review focused on the principal responsibilities of these components.')
page(17);h('4.2 System Architecture')
p('The architecture separates presentation, application processing and persistence. Security checks protect the communication between the browser and the backend. Figure 3 presents the selected technologies and their roles at a basic review level.')
h('Architecture Components',False)
p('<b>User interface:</b> React and TypeScript provide pages and forms; Vite and Tailwind CSS support development and styling. <b>Application logic:</b> Spring Boot processes requests and applies the platform\'s rules. <b>Storage:</b> Spring Data JPA manages PostgreSQL records. <b>Security:</b> Spring Security restricts authenticated operations.')
figure('architecture','System architecture and technology layers',350)
p('The browser sends requests to the Java service and displays the returned information. The service checks the user and requested action before accessing the database. Public event responses are separated from private registrations and administrative information.')
page(18);h('4.3 System File Structure')
p('The repository separates frontend code, backend code and supporting files. The following abbreviated tree retains the main implemented paths and shows how the two application layers are organized. Detailed source listings are not required for this overview.')
structure=[(0,'Campus Commons/'),(1,'frontend/'),(2,'src/'),(3,'main.tsx, api.ts, auth.tsx, types.ts'),(3,'pages/'),(4,'Discovery.tsx, EventDetail.tsx, Clubs.tsx'),(4,'AuthPages.tsx, Student.tsx, Profile.tsx'),(4,'ClubWorkspace.tsx, EventEditor.tsx, Admin.tsx'),(3,'components/ - shared controls and layout'),(3,'styles/ - responsive presentation'),(1,'backend/'),(2,'pom.xml'),(2,'src/main/java/edu/campus/'),(3,'CampusApplication.java, SecurityConfig.java'),(3,'AuthController.java, CatalogController.java'),(3,'AdminController.java, RuntimeController.java'),(3,'AuthService.java, CatalogService.java'),(3,'RegistrationService.java, Repositories.java'),(3,'User.java, Club.java, Event.java'),(3,'Membership.java, Registration.java'),(3,'Payment.java, ResetToken.java, PaymentProvider.java'),(2,'src/main/resources/'),(3,'application.properties'),(3,'db/migration/ - database schema changes'),(1,'docs/ - product and technical documentation'),(1,'scripts/ - project commands'),(1,'README.md')]
for depth,t in structure:
 sty=ParagraphStyle('tree',parent=S['p'],leading=17,spaceAfter=0,leftIndent=depth*15)
 pages[pg].append(Paragraph(html.escape(t),sty))
gap(12);p('Frontend pages correspond to student, club and administrator tasks. Backend controllers, services and data classes support the same functional areas, making their relationship easier to review.')
page(19);h('1. Frontend Layer',False)
p('The frontend handles presentation, navigation and user interaction. React pages organize the event catalog, club directory, account forms and role-specific workspaces. TypeScript models describe the information exchanged with the backend.')
p('Reusable controls provide labelled fields, dialogs, loading states and error messages. Tailwind CSS and project styles support consistent layouts on different screen sizes. The API helper connects user actions to the corresponding backend requests.')
h('2. Backend Layer',False)
p('The backend is implemented in Java using Spring Boot. Controllers receive requests and return structured responses. Services apply rules for approval, ownership, event publication and registration. This keeps the application\'s decisions separate from the visual interface.')
p('Spring Data JPA supports retrieval and updating of persistent records. Data classes represent users, clubs, events, memberships, registrations and payment information. PostgreSQL retains these records, while schema migration files document the database structure.')
h('3. Security &amp; Integration',False)
p('Spring Security manages authenticated access. Students can inspect their own registrations, clubs can manage their own events, and administrators receive review and moderation controls. The service checks these permissions when handling a request.')
p('The API layer connects React to Spring Boot. The frontend reports the result of an operation after the backend has processed it. This arrangement avoids relying on browser controls alone to protect records or determine event availability.')
p('A separate payment-provider interface supports the fee-related part of registration. The current implementation uses a development simulator. PostgreSQL may be hosted locally or through Supabase, while account access and application rules remain in the Java backend.')
page(20);h('4.4 Key System Components')
p('The platform consists of five related functional components. Each component has a clear responsibility and shares the records needed to complete the college event-management process.')
h('1. Identity and Profile Module',False)
p('This component supports signup, login, logout and profile maintenance. Students provide basic college details used in event eligibility. The frontend collects information through labelled forms, while the backend validates it and controls access to the account.')
h('2. Club Module',False)
p('Clubs maintain their names, descriptions, categories and contact information. Students can browse approved clubs and join or leave them. Administrative approval controls publication privileges, separating organization review from ordinary student participation.')
h('3. Event Module',False)
p('Clubs create, edit and publish events with a date, venue, capacity, fee and eligibility conditions. The public interface presents these details for discovery. The backend checks ownership and publication status so that an organizer manages only its own activities.')
h('4. Registration and Payment Module',False)
p('Students register for eligible events and view the resulting status. Free events are confirmed directly. Fee-based events use the available simulated payment facility, which records the outcome without collecting money. Cancellation and registration history remain connected to the event record.')
h('5. Dashboard and Administration Module',False)
p('Student dashboards present commitments and memberships. Club workspaces present owned events and participant records. Administrative screens support user review, club approval and event moderation. Together, these views make the same underlying information accessible according to each role\'s responsibility.')

# Contents and lists refer only to retained sections, never to later template chapters.
roman=['i','ii','iii','iv','v','vi','vii']
def label(n):return roman[n-1] if n<=7 else str(n-7)
def listing(rows):
 data=[[Paragraph(t,S['cell']),Paragraph(v,S['cell'])] for t,v in rows]
 t=Table(data,colWidths=[412,56],hAlign='LEFT');t.setStyle(TableStyle([('GRID',(0,0),(-1,-1),.5,colors.grey),('BACKGROUND',(0,0),(-1,-1),colors.white),('VALIGN',(0,0),(-1,-1),'TOP'),('LEFTPADDING',(0,0),(-1,-1),7),('RIGHTPADDING',(0,0),(-1,-1),7),('TOPPADDING',(0,0),(-1,-1),5),('BOTTOMPADDING',(0,0),(-1,-1),5)]));pages[pg].append(t)
page(3);h('Table of Contents',False)
listing([('<b>Section</b>','<b>Page</b>'),('Title Page','i'),('Certificate','ii'),('Index (Table of Contents)','iii-iv'),('List of Figures','v'),('List of Tables','vi'),('Abstract','vii')]+[(t,label(n)) for t,n in headings if 8<=n<=12])
page(4);h('Table of Contents (continued)',False)
listing([('<b>Section</b>','<b>Page</b>')]+[(t,label(n)) for t,n in headings if n>=13])
page(5);h('List of Figures',False);listing([('<b>Figure</b>','<b>Page</b>')]+[(t,label(n)) for t,n in figures])
page(6);h('List of Tables',False);listing([('<b>Table</b>','<b>Page</b>')]+[(t,label(n)) for t,n in tables])

body=D/'reflowed.pdf';c=canvas.Canvas(str(body),pagesize=(612,792),pageCompression=1,initialFontName='TNR',initialFontSize=12);c.setTitle('College Event Management Website - Basic Project Review');c.setAuthor('');positions=[];over=[]
for num in range(1,21):
 c.saveState();c.setFillAlpha(.30);c.drawImage(str(A/'watermark.png'),189,277,234,238,mask='auto');c.restoreState()
 if num>1:c.setFont('TNR',12);c.drawRightString(540,757,label(num))
 y=728
 for item in pages[num]:
  y-=item.getSpaceBefore();ww,hh=item.wrap(468,700)
  if y-hh<48:over.append((num,round(y-hh,1),getattr(item,'text','')[:65]))
  item.drawOn(c,72+(468-ww)/2 if isinstance(item,Image) else 72,y-hh);positions.append((num,round(y,2),round(y-hh,2),getattr(item,'text','')));y-=hh+item.getSpaceAfter()
 c.showPage()
c.save()
if over:raise RuntimeError(over)
r=PdfReader(body);w=PdfWriter();w.append(r);w.set_page_label(0,6,style='/r',start=1);w.set_page_label(7,19,style='/D',start=1)
# Remove the unused default font so the resource inventory is Times-only too.
for pp in w.pages:
 fonts=pp['/Resources']['/Font']
 regular=next(k for k,v in fonts.items() if str(v.get_object().get('/BaseFont','')).endswith('TimesNewRomanPSMT'))
 stream=ContentStream(pp.get_contents(),w)
 for operands,operator in stream.operations:
  if operator==b'Tf' and operands[0]=='/F3':operands[0]=NameObject(regular)
 pp[NameObject('/Contents')]=w._add_object(stream)
 for key in list(fonts):
  if fonts[key].get_object().get('/BaseFont')=='/Helvetica':del fonts[key]
w.add_metadata({'/Title':'College Event Management Website - Basic Project Review','/Subject':'Revised report limited to original template pages 1-30','/Author':''})
for title,n in headings:w.add_outline_item(title,n-1)
with OUT.open('wb') as f:w.write(f)
json.dump({'headings':headings,'figures':figures,'tables':tables,'positions':positions,'source':'College_Event_Management_Project_Report_Times_New_Roman.pdf','scope_end':'4.4 Key System Components','template_last_page':30},open(D/'manifest.json','w'),indent=2)
print('Saved',OUT,'20 pages; Times New Roman 15 pt headings / 12 pt body.')
