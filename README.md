# Phenotype




<!--[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]-->
[![MIT License][license-shield]][license-url]
[![LinkedIn][linkedin-shield]][linkedin-url]



<!-- PROJECT LOGO -->
<br />
<p align="center">
  <a href="https://github.com/glasgowm148/Phenotype">
    <img src="Phenotype/data/img/logo.png" alt="Logo" width="80" height="80">
  </a>

  <h3 align="center">Phenotype</h3>

  <p align="center">
    A proof-of-concept fake news detection cog for RedBot
    <br />
    <a href="https://github.com/glasgowm148/Phenotype/tree/main/Phenotype/data/docs"><strong>Explore the docs »</strong></a>
    <br />
    <br />
    <a href="https://github.com/glasgowm148/Phenotype/data/demo">View Demo</a>
    ·
    <a href="https://github.com/glasgowm148/Phenotype/issues">Report Bug</a>
    ·
    <a href="https://github.com/glasgowm148/Phenotype/issues">Request Feature</a>
  </p>
</p>



<!-- TABLE OF CONTENTS -->
<details open="open">
  <summary><h2 style="display: inline-block">Table of Contents</h2></summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#roadmap">Roadmap</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
    <li><a href="#acknowledgements">Acknowledgements</a></li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## About The Project

![Phenotype Screen Shot](https://github.com/glasgowm148/Phenotype/blob/master/data/phenotype.png)


### Built With

## Jupyter Notebook

There's two Jupyter notebooks which are pretty much functional. Retrieving 500-1k rsids a second using [MyVariant.info](https://myvariant.info/) which [returns XML](http://myvariant.info/v1/variant/rs9264942)

Currently exports a plain HTML table, NaN and 23andme i-rsid's dropped and sorted by adviser rating.

![](https://github.com/glasgowm148/Phenotype/blob/master/data/html_table.png)

### Scrape & Save

[Scrape & Save](https://github.com/glasgowm148/Phenotype/blob/master/DNA%20Pandas/Scrape_and_Save.ipynb) queries your rsids against ClinVar and returns assosciations, risk allele's, frequency - and stores it in a datatable. 

### Load & Analyse

[Load & Analyse](https://github.com/glasgowm148/Phenotype/blob/master/DNA%20Pandas/Load_and_Analyse%20.ipynb) matches your rsids against the ClinVar dataframe pulled from [Scrape & Save](https://github.com/glasgowm148/Phenotype/blob/master/DNA%20Pandas/Scrape_and_Save.ipynb). This can be exported to CSV or HTML.

### Limitations

Currently only tested with 23andme V4 & V5. 


### ToDo 

* Beautify HTML datatable using DataTables
* Flatten all DTC file formats into a consistent dataframe for manipulation
* Add more sources of data
  * SNPedia
  * ONIM
* Data-validaiton
  * strand orientation
  * risk allelle debugging

<!-- GETTING STARTED -->
## Getting Started
### Installation




<!-- USAGE EXAMPLES -->
## Overview





<!-- ROADMAP -->
## Roadmap

See the [open issues](https://github.com/glasgowm148/Phenotype/issues) for a list of proposed features (and known issues).



<!-- CONTRIBUTING -->
## Contributing

Contributions are what make the open source community such an amazing place to be learn, inspire, and create. Any contributions you make are **greatly appreciated**.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request



<!-- LICENSE -->
## License

Distributed under the MIT License. See `LICENSE` for more information.



<!-- CONTACT -->
## Contact

Mark Glasgow - markglasgow@gmail.com


<!-- ACKNOWLEDGEMENTS -->
## Acknowledgements





<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[contributors-shield]: https://img.shields.io/github/contributors/glasgowm148/Phenotype.svg?style=for-the-badge
[contributors-url]: https://github.com/glasgowm148/Phenotype/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/glasgowm148/Phenotype.svg?style=for-the-badge
[forks-url]: https://github.com/glasgowm148/Phenotype/network/members
[stars-shield]: https://img.shields.io/github/stars/glasgowm148/Phenotype.svg?style=for-the-badge
[stars-url]: https://github.com/glasgowm148/Phenotype/stargazers
[issues-shield]: https://img.shields.io/github/issues/othneildrew/Best-README-Template.svg?style=for-the-badge
[issues-url]: https://github.com/glasgowm148/Phenotype/issues
[license-shield]: https://img.shields.io/github/license/othneildrew/Best-README-Template.svg?style=for-the-badge
[license-url]: https://github.com/glasgowm148/Phenotype/blob/master/LICENSE.txt
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555
[linkedin-url]: https://www.linkedin.com/in/glasgowmark/