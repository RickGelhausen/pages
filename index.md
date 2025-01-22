---
layout: default
title: SPP2002 (Z2 Project)
---

<h1 class="mb-5">Publication List</h1>

<div class="publications-list">
    {% assign sorted_publications = site.data.publications | sort: "year" | reverse %}
    {% for publication in sorted_publications %}
    {% include publication-entry.html publication=publication %}
    {% endfor %}
</div>

