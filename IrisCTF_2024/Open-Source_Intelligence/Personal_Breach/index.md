# Personal Breach [173 Solves]

## Description

![chal.png](img/chal.png)

> Security questions can be solved by reconnaissance. The weakest link in security could be the people around you.
>
> <https://personal-breach-web.chal.irisc.tf/>
>
> By: Lychi

## Solution

### Initial Analysis

![1.png](img/1.png)

> How old is Iris?
>
> What hospital was Iris born in?
>
> What company does Iris work for?

We need to answer the three questions.
I will try to search about Iris Stein.
I believe this is a continuation of [Away on Vacation](../Away_on_Vacation/index.md), so it seems necessary to investigate Michel, who is Iris's assistant, too.

### 1. How old is Iris?

- Michel's Instagram account: <https://www.instagram.com/michelangelo_corning/>

Michel follows Iris.

![michel_followers.png](img/michel_followers.png)

Iris posts the name of their mother:

<https://www.instagram.com/p/C1qwh0Cuj5P/>

![iris_post.png](img/iris_post.png)

> @/ElainaStein

Elaina, Iris's mother, has facebook account:

- Elaina Facebook: <https://www.facebook.com/profile.php?id=61555040318052>

![elaina_facebook.png](img/elaina_facebook.png)

Elaina posts Iris's birth: <https://www.facebook.com/permalink.php?story_fbid=pfbid0mG3qxXeHCF3biXuWaaxaFvJjrQ2TXDVLokV76WvUHrk4XS8b8V8mzadad2PfFdaZl&id=61555040318052>

![elaina_facebook_iris_birth.png](img/elaina_facebook_iris_birth.png)

> Elaina Stein
>
> April 28, 1996
>
> A day to remember and share. Iris's day!
>
> April 27, 1996
>
> Elaina Stein
>
> I still remember Iris coming into the world. It all happened so fast on a cold day, one minute I was stuck in traffic and the next I was rushed to the closest hospital. Her dad had to rush over from work to help with the delivery. Everything is a blur but seeing her face was truly something.
>
> To think they got ranked to be the best maternity hospital in Manhattan is astounding. They even renovated the rooms 🥹

Iris was born in 1996/4/27 so it's 27-yeas-old in 2024/1/7.

1st Answer: 27

### 2. What hospital was Iris born in?

Elaina's post in Facebook describes the maternity hospital in Manhattan.
The maternity hospital is one of the top 10 in Manhattan.

[TOP 10 BEST Maternity Hospitals in Manhattan, NY - January 2024 - Yelp](https://www.yelp.com/search?find_desc=Maternity+Hospitals&find_loc=Manhattan%2C+NY)

![maternity_hospital.png](img/maternity_hospital.png)

2nd Answer: Lenox Hill Hospital

### 3. What company does Iris work for?

Search DuckDuckGo `iris stein assistant` query: <https://duckduckgo.com/?q=iris+stein+assistant&t=h_&ia=web>

- Iris's Linkedin Account: <https://www.linkedin.com/in/iris-stein-57894b2a7/>

![iris_linkedin.png](img/iris_linkedin.png)

3rd Answer: Mountain Peak Hiring Agency

## Flag

![flag.png](img/flag.png)

irisctf{s0c1al_m3d1a_1s_an_1nf3cti0n}
