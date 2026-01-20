
PROMPT_FOR_DOMAIN_TEMPLATE = """I have a domain description in natural language. I want to get a domain template on PDDL. For example

Domain NL:  
```markdown
### Context
A bank client wants to take a loan for a certain amount with a repayment schedule and interest rate. The bank needs to check the client's creditworthiness, approve the application, disburse the funds, and manage repayments.

***

### Objects
- Clients
- Loan applications
- Loans
- Payments
- Client accounts

***

### Goal
- Loan granted to the client
- All payments completed according to the schedule

***

### Inputs
- Client submits a loan application
- Bank checks creditworthiness
- If approved, loan is created and funds are credited to the client's account
- Client makes payments according to the repayment schedule
- When all payments are made, the loan is considered repaid

***

### Possible Actions

- Submit loan application
- Check creditworthiness
- Approve application
- Disburse loan
- Make payment
- Verify payments
- Close loan

***

### Example Predicates

- (application_submitted ?c - Client ?a - LoanApplication)
- (creditworthiness_checked ?a - LoanApplication)
- (application_approved ?a - LoanApplication)
- (loan_disbursed ?l - Loan)
- (payment_due ?p - Payment)
- (payment_made ?p - Payment)
- (loan_closed ?l - Loan)

***

### Brief Process Description

1. Client submits a loan application.
2. Bank verifies the application.
3. If approved, a loan is created.
4. Loan funds are disbursed to the client's account.
5. Client makes payments as scheduled.
6. After all payments, the loan is closed.
```

Domain PDDL Template:
```pddl
(define (domain banking-loans)
  (:requirements :strips :typing :universal-preconditions)

  (:types
    client loanapplication loan payment payment_schedule - object
  )
  (:predicates)
  
  (:action submit-application
    :parameters (?c - client ?a - loanapplication)
    :precondition ()
    :effect ()
  )
  
  (:action check-creditworthiness
    :parameters (?a - loanapplication)
    :precondition ()
    :effect ()
  )
  
  (:action approve-application
    :parameters (?a - loanapplication)
    :precondition ()
    :effect ()
  )
  
  (:action disburse-loan
    :parameters (?c - client ?l - loan ?a - loanapplication)
    :precondition ()
    :effect ()
  )
  
  (:action make-payment
    :parameters (?p - payment ?l - loan)
    :precondition ()
    :effect ()
  )
  
  (:action verify-payments
    :parameters (?l - loan)
    :precondition ()
    :effect ()
  )
  
  (:action close-loan
    :parameters (?l - loan)
    :precondition ()
    :effect ()
  )
)
```

Here is the description of the target template on NL:  
```markdown
{target_domain_nl}
```
Keep in mind that there are gaps in the templates that need to be left blank. Also keep in mind that the domain must cover all tasks.
create a template for the domain for me. Actions should not contain preconditions and consequences. 

mandatory conditions:
1. The predicate field must be : "(:predicates)" (without comments inside)

2. There should be fields for each action 
    :precondition ()
    :effect ()

3. The domain must include all of these types and everything actions must contain only these types:
{types_in_templates}

"""

PROMPT_FOR_TASKS_TEMPLATE = """Now generate me templates for the tasks.

init and goal should look exactly like this:
"(:init )"
"(:goal (and ))"

Keep in mind that it is necessary to declare the objects used and determine their type according to the domain.
Think of all the objects that may be useful to achieve the goal.
Do not output any information other than the template to the PDDL.
Objects that have the same meaning must have the same types.

Task on NL:
```markdown
You are tasked with a repayment plan:

Initially:  
- The client has a $30,000 loan.  

Your goal is to repay by:  
- 18 monthly payments not exceeding $2,000 each.
```

Task template on PDDL
```pddl
(define (problem loan-task)
(:domain banking-loans)
(:objects some_client - client some_loanApp - loanapplication some_loan - loan
    payment1 payment2 payment3 payment4 payment5 payment6
    payment7 payment8 payment9 payment10 payment11 payment12
    payment13 payment14 payment15 payment16 payment17 payment18 - payment)
(:init )
(:goal (and ))
)
```

Target tasks on NL:
```markdown
{tasks_nl}
```
"""

PROMPT_FOR_GENERATE_TASK_NL = """Generate 10 tasks in natural language. The tasks should 
1. Be plan-oriented. Tasks should not be based on numbers.
2. Have an economic, business, or banking background.
3. Have different plan lengths (There is no need to come up with a plan for tasks, tasks can be ranked by difficulty)
4. The actions used in the plans should not be repeated more than 3 times.
5. The formulations should contain a detailed description of the essence of the task, the input data, and the goal.
6. Each task should be wrapped in markdown.

Keep in mind that for each step it is necessary to consider which checks need to be performed.


A: B2B project planning
B:
```markdown
You are tasked with managing a B2B software integration project with the following conditions:

Initially:  
- Your company provides cloud-based CRM software.  
- A new client, a logistics company, has signed a contract for a CRM integration.  

Your goal is to complete the project with:  
- 3 project phases over 6 weeks.  
- Each phase must include planning, execution, and a client review.  
- The final delivery must include a full data migration, user training session, and performance testing.  
```

A:
{topic}
"""

PROMPT_FOR_GENERATE_DOMAIN_NL = """
Now describe in natural language the domain that will be compiled in PDDL to solve these problems. 
The domain must cover all tasks simultaneously. Its description should be wrapped in markdown.

Here is an example of domain:
```markdown
### Context
A bank client wants to take a loan for a certain amount with a repayment schedule and interest rate. The bank needs to check the client's creditworthiness, approve the application, disburse the funds, and manage repayments.

***

### Objects
- Clients
- Loan applications
- Loans
- Payments
- Client accounts

***

### Goal
- Loan granted to the client
- All payments completed according to the schedule

***

### Inputs
- Client submits a loan application
- Bank checks creditworthiness
- If approved, loan is created and funds are credited to the client's account
- Client makes payments according to the repayment schedule
- When all payments are made, the loan is considered repaid

***

### Possible Actions

- Submit loan application
- Check creditworthiness
- Approve application
- Disburse loan
- Make payment
- Verify payments
- Close loan

***

### Example Predicates

- (application_submitted ?c - Client ?a - LoanApplication)
- (creditworthiness_checked ?a - LoanApplication)
- (application_approved ?a - LoanApplication)
- (loan_disbursed ?l - Loan)
- (payment_due ?p - Payment)
- (payment_made ?p - Payment)
- (loan_closed ?l - Loan)

***

### Brief Process Description

1. Client submits a loan application.
2. Bank verifies the application.
3. If approved, a loan is created.
4. Loan funds are disbursed to the client's account.
5. Client makes payments as scheduled.
6. After all payments, the loan is closed.
```
"""


PROMT_FOR_FIX_DOMAIN_AND_TASK = """I have a domain like this on PDDL:
```pddl
{domain_pddl}
```

And that's the problem on PDDL: 
```pddl
{task_pddl}
```

And its formulation in natural language:
```markdown
{task_nl}
```

If I run the fast-downward scheduler on this issue and domain, I will get this error:
```markdown
{error}
```

Fix the domain and the problem so that you can create a plan for the problem in this domain. Keep in mind that this domain is also used for other tasks, so when you change it, try to add new actions (even if they are very similar), but do not delete them. If the action is written incorrectly (non-matching types or syntax violation), then you can replace it. 
if the action needs to be changed, then print a new action with the same name. If you need to add an action, then write a new action.
If necessary, correct the correspondence of the domain name in the ad and the problem. Tasks should not be based on numbers.

Your answer should have the format:  
```pddl
here new problem
```
```pddl
here added and replaced actions in the domain
```
"""


PROMPT_FOR_GENERATE_DOMAIN_AND_TASK_PDDL = """I have an empty domain template on PDDL:
```pddl
{domain_template_pddl}
```

And an empty problem template on PDDL:
```pddl
{task_template_pddl}
```

And the formulation of the problem in natural language:
```pddl
{task_nl}
```
You must fill out these templates in such a way that the problem in PDDL preserves the essence of the problem in natural language and is solvable in the domain (you can create a plan to achieve the goal).  You can add new actions. Try not to create too general actions: if an action can be divided into several, then it must be divided.

Your response should have the following format:
```pddl
here new problem
```
```pddl
here new domain
```
"""

def create_format():
    payment_domain_template_path = '/home/max/work_area/course_work/rag_bencmark/data/domains/payments/domain_template.pddl'
    payment_task_template_path = '/home/max/work_area/course_work/rag_bencmark/data/domains/payments/p01_template.pddl'
    payment_task_nl_path = '/home/max/work_area/course_work/rag_bencmark/data/domains/payments/p01.nl'
    paths = [payment_domain_template_path, payment_task_template_path, payment_task_nl_path]
    res = []
    for path in paths:
      with open(path, 'r') as f:
         res.append(f.read())
    return res

args = create_format()
ONE_SHOT_PROMPT_FOR_GENERATE_DOMAIN_AND_TASK_PDDL = PROMPT_FOR_GENERATE_DOMAIN_AND_TASK_PDDL.format(domain_template_pddl=args[0], task_template_pddl=args[1], task_nl=[args[2]])

ONE_SHOT_GENERATE_DOMAIN_AND_TASK_PDDL_ANSWER = """```pddl
(define (problem loan-task-1)
  (:domain banking-loans)
(:objects some_client - client some_loanApp - loanapplication some_loan - loan payment1 payment2 payment3 - payment)
  (:init
    ; The client has no outstanding loans.
    (not (loan_closed some_loan))
    ; The client applies for a loan of $10,000.
    (not (application_submitted some_client some_loanApp))
    (not (creditworthiness_checked some_loanApp))
    (not (application_approved some_loanApp))
    (not (loan_disbursed some_loan))
    ; Payments are due for the loan.
    (payment_due payment1)
    (payment_due payment2)
    (payment_due payment3)
    (not (payment_made payment1))
    (not (payment_made payment2))
    (not (payment_made payment3))
  )
  (:goal (and
    ; The goal is to complete the loan repayment.
    (loan_closed some_loan)
    (payment_made payment1)
    (payment_made payment2)
    (payment_made payment3)
  ))
)
```
```pddl
(define (domain banking-loans)
    (:requirements :action-costs :strips :typing :universal-preconditions)
    (:types client loan loanapplication payment payment_schedule - object)
    (:predicates (application_approved ?a - loanapplication)  (application_submitted ?c - client ?a - loanapplication)  (creditworthiness_checked ?a - loanapplication)  (loan_closed ?l - loan)  (loan_disbursed ?l - loan)  (payment_due ?p - payment)  (payment_made ?p - payment))
    (:action approve-application
        :parameters (?a - loanapplication)
        :precondition (and (creditworthiness_checked ?a) (not (application_approved ?a)))
        :effect (and (application_approved ?a))
    )
     (:action check-creditworthiness
        :parameters (?c - client ?a - loanapplication)
        :precondition (and (application_submitted ?c ?a) (not (creditworthiness_checked ?a)))
        :effect (and (creditworthiness_checked ?a))
    )
     (:action close-loan
        :parameters (?l - loan)
        :precondition (and (loan_disbursed ?l) (not (loan_closed ?l)))
        :effect (and (loan_closed ?l))
    )
     (:action disburse-loan
        :parameters (?c - client ?l - loan ?a - loanapplication)
        :precondition (and (application_approved ?a) (not (loan_disbursed ?l)))
        :effect (and (loan_disbursed ?l))
    )
     (:action make-payment
        :parameters (?p - payment ?l - loan)
        :precondition (and (payment_due ?p) (loan_disbursed ?l) (not (payment_made ?p)))
        :effect (and (payment_made ?p))
    )
     (:action submit-application
        :parameters (?c - client ?a - loanapplication)
        :precondition (not (application_submitted ?c ?a))
        :effect (and (application_submitted ?c ?a))
    )
     (:action verify-payments
        :parameters (?l - loan)
        :precondition (and (loan_disbursed ?l) (not (loan_closed ?l)))
        :effect (and (loan_closed ?l))
    )
)
```
"""