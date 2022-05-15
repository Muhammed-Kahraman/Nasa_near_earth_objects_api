# Asteroids - NeoWs Rest Api

Retrieve a json array of Asteroids special information ordered by the their closest passing point to (km) to Earth.

- Which information you can get with this API?
      Asteroids name,
      Closest approach date,
      Closest passing point (km) from Earth, 
      Min Estimated diameter (km) and max Estimated diameter (km)

Date format: YYYY-MM-DD
Maximum possible day between start date and end date: 7


<p dir="auto"> </p>
<h3 dir="auto"><a id="user-content-virtualenv-environment-" class="anchor" aria-hidden="true" href="#virtualenv-environment-"><svg class="octicon octicon-link" viewBox="0 0 16 16" version="1.1" width="16" height="16" aria-hidden="true"><path fill-rule="evenodd" d="M7.775 3.275a.75.75 0 001.06 1.06l1.25-1.25a2 2 0 112.83 2.83l-2.5 2.5a2 2 0 01-2.83 0 .75.75 0 00-1.06 1.06 3.5 3.5 0 004.95 0l2.5-2.5a3.5 3.5 0 00-4.95-4.95l-1.25 1.25zm-4.69 9.64a2 2 0 010-2.83l2.5-2.5a2 2 0 012.83 0 .75.75 0 001.06-1.06 3.5 3.5 0 00-4.95 0l-2.5 2.5a3.5 3.5 0 004.95 4.95l1.25-1.25a.75.75 0 00-1.06-1.06l-1.25 1.25a2 2 0 01-2.83 0z"></path></svg></a><code>virtualenv</code> environment <a name="user-content-virtualenv"></a></h3>
<ol dir="auto">
<li>Clone the repo</li>
</ol>
<div class="highlight highlight-source-shell position-relative overflow-auto" data-snippet-clipboard-copy-content="git clone https://github.com/nasa/apod-api"><pre>git clone https://github.com/Muhammed-Kahraman/Nasa_near_earth_objects_api.git</pre></div>
<ol start="2" dir="auto">
<li><code>cd</code> into the new directory</li>
</ol>
<div class="highlight highlight-source-shell position-relative overflow-auto" data-snippet-clipboard-copy-content="cd apod-api"><pre><span class="pl-c1">cd</span> Nasa_near_earth_objects_api </pre></div>
<ol start="3" dir="auto">
<li>Create a new virtual environment <code>env</code> in the directory</li>
</ol>
<div class="highlight highlight-source-shell position-relative overflow-auto" data-snippet-clipboard-copy-content="python -m virtualenv env"><pre>python -m virtualenv env</pre></div>
<ol start="4" dir="auto">
<li>Activate the new environment</li>
</ol>
<div class="highlight highlight-source-shell position-relative overflow-auto" data-snippet-clipboard-copy-content="source env/bin/activate"><pre><span class="pl-c1">source</span> .\venv\Scripts\activate </pre></div>
<ol start="5" dir="auto">
<li>Install dependencies in new environment</li>
</ol>
<div class="highlight highlight-source-shell position-relative overflow-auto" data-snippet-clipboard-copy-content="pip install -r requirements.txt"><pre>pip install -r requirements.txt</pre></div>
<div class="highlight highlight-source-shell position-relative overflow-auto" data-snippet-clipboard-copy-content="pip install -r requirements.txt"><pre>Create a .env file same directory with the project.</pre></div>
<div class="highlight highlight-source-shell position-relative overflow-auto" data-snippet-clipboard-copy-content="pip install -r requirements.txt"><pre>Set up secret_key and nasa apikey inside this file (secret_key = "", apiKey = "")</pre></div>
<ol start="8" dir="auto">
<li>Run the server locally</li>
</ol>
<div class="highlight highlight-source-shell position-relative overflow-auto" data-snippet-clipboard-copy-content="python application.py"><pre>python manage.py runserver </pre></div>
<p dir="auto"> </p>

