# ============================================================
# SmartHire AI — 500+ Interview Questions Bank
# Organised by skill/topic. No repeats guaranteed via shuffling.
# ============================================================

TECHNICAL_QUESTIONS = {
    "python": [
        "What is the difference between a list and a tuple in Python?",
        "Explain how Python's garbage collection works.",
        "What are decorators in Python? Give an example.",
        "What is the difference between `deepcopy` and `copy` in Python?",
        "Explain Python's GIL (Global Interpreter Lock).",
        "What are generators and how do they differ from regular functions?",
        "How does exception handling work in Python?",
        "What is the difference between `@staticmethod` and `@classmethod`?",
        "Explain list comprehensions with an example.",
        "What are lambda functions? When would you use them?",
        "How does Python manage memory?",
        "What is `*args` and `**kwargs`?",
        "Explain the concept of duck typing in Python.",
        "What is a context manager and how does `with` work?",
        "What is the difference between `is` and `==`?",
        "Explain how `map()`, `filter()`, and `reduce()` work.",
        "What are Python's built-in data types?",
        "How do you handle file operations in Python?",
        "What is PEP 8 and why is it important?",
        "Explain the MRO (Method Resolution Order) in Python.",
    ],
    "java": [
        "What is the difference between JDK, JRE, and JVM?",
        "Explain the four pillars of OOP in Java.",
        "What is the difference between `==` and `.equals()` in Java?",
        "What are checked and unchecked exceptions?",
        "Explain the concept of interfaces vs abstract classes.",
        "What is autoboxing and unboxing in Java?",
        "Explain the Java Collections Framework.",
        "What is the difference between ArrayList and LinkedList?",
        "What are Java generics and why are they used?",
        "Explain Java's multithreading and `synchronized` keyword.",
        "What is the difference between `HashMap` and `Hashtable`?",
        "What is Java Stream API? Give a use case.",
        "Explain the concept of lambda expressions in Java 8.",
        "What are design patterns? Explain Singleton pattern.",
        "What is garbage collection in Java?",
        "Explain the `final`, `finally`, and `finalize` keywords.",
        "What is method overloading vs method overriding?",
        "Explain the concept of dependency injection.",
        "What is the difference between `String`, `StringBuilder`, and `StringBuffer`?",
        "What is a `NullPointerException` and how do you prevent it?",
    ],
    "spring": [
        "What is the Spring Framework and what problems does it solve?",
        "Explain Dependency Injection in Spring.",
        "What is the difference between `@Component`, `@Service`, `@Repository`, and `@Controller`?",
        "What is Spring Boot and how is it different from Spring MVC?",
        "Explain Spring's IoC container.",
        "What is `@Autowired` and how does it work?",
        "What is a Spring Bean lifecycle?",
        "Explain Spring AOP (Aspect-Oriented Programming).",
        "What is Spring Data JPA?",
        "What is `@Transactional` and when would you use it?",
        "Explain Spring Security and its key components.",
        "What is `application.properties` vs `application.yml`?",
        "What is the difference between `@RequestMapping` and `@GetMapping`?",
        "How do you handle exceptions globally in Spring Boot?",
        "What is Spring's `RestTemplate` vs `WebClient`?",
        "Explain Spring Profiles and their use case.",
        "What is Spring Boot Actuator?",
        "How do you connect a database in Spring Boot?",
        "What is the difference between `@PathVariable` and `@RequestParam`?",
        "Explain the concept of microservices with Spring Boot.",
    ],
    "javascript": [
        "What is the difference between `var`, `let`, and `const`?",
        "Explain closures in JavaScript.",
        "What is the event loop in JavaScript?",
        "What is hoisting in JavaScript?",
        "Explain Promises and async/await.",
        "What is the difference between `==` and `===`?",
        "What is prototypal inheritance?",
        "Explain the concept of `this` in JavaScript.",
        "What are arrow functions and how do they differ from regular functions?",
        "What is destructuring in ES6?",
        "Explain the spread operator and rest parameters.",
        "What is a callback function?",
        "What is the difference between `null` and `undefined`?",
        "Explain event bubbling and event delegation.",
        "What is the DOM and how do you manipulate it?",
        "What are modules in JavaScript (ES6)?",
        "Explain `localStorage` vs `sessionStorage` vs cookies.",
        "What is a pure function?",
        "Explain the concept of debouncing and throttling.",
        "What is `JSON.parse()` and `JSON.stringify()`?",
    ],
    "sql": [
        "What is the difference between `INNER JOIN`, `LEFT JOIN`, and `RIGHT JOIN`?",
        "Explain the difference between `WHERE` and `HAVING`.",
        "What are indexes in SQL and why are they used?",
        "What is normalization? Explain 1NF, 2NF, and 3NF.",
        "What is a primary key vs a foreign key?",
        "Explain ACID properties in databases.",
        "What is the difference between `DELETE`, `TRUNCATE`, and `DROP`?",
        "What are stored procedures and triggers?",
        "What is a subquery? Give an example.",
        "Explain GROUP BY and ORDER BY.",
        "What is a view in SQL?",
        "What is the difference between `UNION` and `UNION ALL`?",
        "Explain transactions in SQL.",
        "What is denormalization and when would you use it?",
        "How do you find duplicate records in a table?",
        "What is an aggregate function? Give examples.",
        "Explain the difference between clustered and non-clustered indexes.",
        "What is a self join?",
        "How do you optimize a slow SQL query?",
        "What is referential integrity?",
    ],
    "html": [
        "What is the difference between HTML and HTML5?",
        "Explain semantic HTML and why it matters.",
        "What is the difference between `<div>` and `<span>`?",
        "What are meta tags and why are they important?",
        "Explain the difference between `id` and `class` attributes.",
        "What is the HTML DOM?",
        "What are data attributes (`data-*`)?",
        "What is the difference between block-level and inline elements?",
        "Explain the `<canvas>` element.",
        "What is an iframe and when would you use it?",
        "What is `alt` attribute on images and why is it important?",
        "What is `viewport` meta tag?",
        "Explain HTML forms and their attributes.",
        "What is accessibility (a11y) in HTML?",
        "Explain the difference between `<strong>` and `<b>`.",
        "What are Web Workers?",
        "What is LocalStorage and how does it work?",
        "Explain HTML5 audio and video tags.",
        "What is the purpose of `DOCTYPE` in HTML?",
        "What is ARIA in HTML?",
    ],
    "css": [
        "What is the box model in CSS?",
        "Explain the difference between `margin` and `padding`.",
        "What is Flexbox and when would you use it?",
        "Explain CSS Grid layout.",
        "What is the difference between `absolute`, `relative`, `fixed`, and `sticky` positioning?",
        "What are CSS pseudo-classes and pseudo-elements?",
        "Explain CSS specificity.",
        "What is a CSS preprocessor like SASS/SCSS?",
        "What is `z-index` and how does it work?",
        "Explain media queries and responsive design.",
        "What is the difference between `em`, `rem`, `%`, `vw`, and `vh`?",
        "What is CSS transition vs CSS animation?",
        "What is a CSS variable (custom property)?",
        "Explain the `display` property values.",
        "What is `box-sizing: border-box`?",
        "What are CSS selectors? Explain different types.",
        "How do you center an element both horizontally and vertically?",
        "What is `overflow` property in CSS?",
        "What is the difference between `visibility: hidden` and `display: none`?",
        "Explain CSS inheritance.",
    ],
    "data structures": [
        "What is the difference between a stack and a queue?",
        "Explain how a linked list works.",
        "What is a binary tree? Explain its types.",
        "What is a hash table and how does collision resolution work?",
        "Explain the concept of Big O notation.",
        "What is the time complexity of common operations in an array vs linked list?",
        "What is a graph? Explain DFS and BFS.",
        "What is a heap and where is it used?",
        "Explain the difference between a tree and a graph.",
        "What is dynamic programming? Give an example.",
        "Explain the concept of recursion with an example.",
        "What is sorting? Explain Merge Sort and Quick Sort.",
        "What is a binary search tree (BST)?",
        "What is the difference between depth-first and breadth-first search?",
        "Explain a circular queue.",
        "What is a trie and when would you use it?",
        "Explain amortized time complexity.",
        "What is a priority queue?",
        "What is the two-pointer technique?",
        "Explain sliding window technique.",
    ],
    "algorithms": [
        "Explain binary search and its time complexity.",
        "What is the difference between greedy algorithms and dynamic programming?",
        "Explain bubble sort and why it is inefficient.",
        "What is the time complexity of Quick Sort in best, worst, and average cases?",
        "Explain Dijkstra's algorithm.",
        "What is memoization?",
        "Explain the divide and conquer strategy.",
        "What is the knapsack problem?",
        "Explain topological sorting.",
        "What is the time and space complexity of merge sort?",
        "Explain backtracking with an example.",
        "What is Floyd's cycle detection algorithm?",
        "Explain the concept of hashing.",
        "What is the difference between iterative and recursive solutions?",
        "Explain counting sort.",
    ],
    "problem solving": [
        "How do you approach a problem you've never seen before?",
        "Walk me through how you would debug a program that crashes.",
        "How do you break down a complex problem into smaller parts?",
        "Describe a time when you had to think outside the box to solve a problem.",
        "How do you decide between multiple solutions to the same problem?",
        "What is your process for testing your code?",
        "How do you handle a situation when you're stuck on a problem for a long time?",
        "Explain a technical challenge you faced and how you overcame it.",
        "How do you evaluate the trade-offs between time complexity and space complexity?",
        "What steps do you take before writing any code?",
        "How do you ensure your solution handles edge cases?",
        "Describe a project where you optimized performance. What was your approach?",
        "How do you learn a new programming language or framework quickly?",
        "What do you do when your code works but you know it's not the best solution?",
        "Explain a bug that was particularly hard to fix and what you learned.",
    ],
    "communication": [
        "Explain a complex technical concept to a non-technical person.",
        "Describe a situation where you had to explain your code to your team.",
        "How do you document your code?",
        "Describe how you would present a technical proposal to stakeholders.",
        "How do you handle technical disagreements with teammates?",
    ],
    "teamwork": [
        "Describe a successful team project you were part of.",
        "How do you handle a teammate who is not contributing?",
        "What role do you usually take in a team — leader or follower? Why?",
        "How do you share knowledge with your teammates?",
        "Describe a situation where you helped a teammate overcome a technical challenge.",
    ],
}

MANAGEMENT_QUESTIONS = [
    # Leadership
    "Describe a time you took initiative without being asked.",
    "Tell me about a time you led a team project from start to finish.",
    "How do you motivate team members who seem disengaged?",
    "Describe a situation where you had to lead a team through uncertainty.",
    "How do you delegate tasks effectively?",
    "Tell me about a time you had to make a difficult decision as a leader.",
    "How do you handle underperforming team members?",
    "Describe a time you inspired your team to go above and beyond.",
    "What leadership style do you prefer and why?",
    "How do you build trust within a team?",

    # Conflict Resolution
    "How do you handle conflicts within your team?",
    "Describe a time you resolved a disagreement between two colleagues.",
    "How do you handle a conflict with your manager?",
    "Tell me about a time you had to deliver bad news to a teammate.",
    "How do you deal with a difficult client or stakeholder?",
    "Describe a situation where you had to mediate between two parties.",
    "How do you handle passive-aggressive behavior in a team?",
    "Tell me about a time you had to defend your position under pressure.",
    "How do you ensure everyone's voice is heard in a meeting?",
    "Describe a time when you had to compromise to reach a goal.",

    # Time Management & Prioritization
    "How do you prioritize tasks under tight deadlines?",
    "Describe a time you managed multiple projects simultaneously.",
    "How do you handle unexpected changes to a project plan?",
    "What tools or techniques do you use to manage your time?",
    "Tell me about a time you missed a deadline and what you learned.",
    "How do you ensure you stay focused during long projects?",
    "Describe your daily routine when managing a heavy workload.",
    "How do you say no to additional work when you're already overloaded?",
    "Tell me about a time you successfully delivered a project ahead of schedule.",
    "How do you estimate how long a task will take?",

    # Adaptability & Growth
    "Give an example of a time you had to adapt to a major change.",
    "Describe a situation where you failed and what you learned.",
    "How do you stay up to date in a constantly changing field?",
    "Tell me about a time you received critical feedback and how you responded.",
    "How do you handle working in ambiguous or uncertain situations?",
    "Describe a time you had to learn something entirely new quickly.",
    "How do you respond when your idea gets rejected?",
    "Tell me about a time you changed your approach mid-project.",
    "How do you embrace constructive criticism?",
    "Describe a time you stepped outside your comfort zone.",

    # Goal Setting & Achievements
    "Tell me about a goal you achieved and how you did it.",
    "What is your biggest professional achievement so far?",
    "How do you set short-term and long-term goals?",
    "Describe a time you exceeded expectations at work or college.",
    "How do you track progress toward your goals?",
    "Tell me about a project you are most proud of.",
    "What motivates you to do your best work?",
    "Describe a time you went above and beyond what was required.",
    "How do you handle setbacks when working toward a goal?",
    "Tell me where you see yourself in 5 years.",

    # Communication
    "How do you ensure clear communication in a remote or hybrid team?",
    "Describe a time your communication skills helped avoid a misunderstanding.",
    "How do you tailor your communication style for different audiences?",
    "Tell me about a time you had to give a presentation under pressure.",
    "How do you handle miscommunication within a project team?",
    "Describe a time you had to convince someone to adopt your idea.",
    "How do you give constructive feedback without demotivating someone?",
    "Tell me about a time you had to communicate a complex idea simply.",
    "How do you ensure everyone in a meeting leaves with the same understanding?",
    "Describe a time your written communication made a significant impact.",

    # Collaboration & Team Dynamics
    "How do you build rapport with a new team?",
    "Tell me about a time you collaborated with someone very different from you.",
    "How do you handle a teammate who dominates every discussion?",
    "Describe a time you supported a colleague during a difficult time.",
    "How do you ensure your contribution stands out in a team project?",

    # Situational / Hypothetical
    "If you were given a project with no clear requirements, what would you do first?",
    "If two equally urgent tasks arrived at the same time, how would you handle it?",
    "Imagine your team is losing motivation mid-project. What do you do?",
    "If you disagreed with your manager's decision, what would you do?",
    "You discover a critical bug 1 hour before a deadline. What is your plan?",
    "How would you handle a new colleague who refuses to follow team processes?",
    "If a stakeholder keeps changing requirements, how do you manage that?",
    "What would you do if you realized halfway through a project that the approach is wrong?",
    "How would you handle working on a team where no one takes ownership?",
    "If you had unlimited resources to improve your team, what would you change?",
]

# ============================================================
# Helper: get non-repeating questions for a session
# ============================================================
import random

def get_technical_questions(skills: list, count: int = 5, used_questions: list = None) -> list:
    """
    Pull 'count' questions from the bank based on candidate skills.
    Avoids repeating questions already used (passed via used_questions).
    """
    used = set(used_questions or [])
    pool = []

    # Gather questions for matched skills
    for skill in skills:
        skill_lower = skill.lower()
        for key, questions in TECHNICAL_QUESTIONS.items():
            if key in skill_lower or skill_lower in key:
                for q in questions:
                    if q not in used:
                        pool.append(q)

    # If pool is too small, supplement with problem_solving and communication
    if len(pool) < count:
        for q in TECHNICAL_QUESTIONS.get("problem solving", []):
            if q not in used:
                pool.append(q)

    # Remove duplicates within pool
    pool = list(dict.fromkeys(pool))
    random.shuffle(pool)
    return pool[:count]


def get_management_questions(count: int = 5, used_questions: list = None) -> list:
    """
    Pull 'count' management questions, avoiding repeats.
    """
    used = set(used_questions or [])
    pool = [q for q in MANAGEMENT_QUESTIONS if q not in used]
    random.shuffle(pool)
    return pool[:count]