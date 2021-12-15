<div id="top"></div>




<!-- PROJECT SHIELDS -->

[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
<img alt="Licence Creative Commons" style="border-width:0" src="https://i.creativecommons.org/l/by-nc/3.0/fr/88x31.png" />
[![LinkedIn][linkedin-shield]][linkedin-url]



<!-- PROJECT LOGO -->
<br />
<div align="center">
  <!--<a href="https://github.com/Torilen/French-Dialogue-Dataset"> -->
  <!--  <img src="images/logo.png" alt="Logo" width="80" height="80"> -->
  <!--</a> -->

  <h3 align="center">French Dialogue Dataset</h3>


</div>



<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
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
    <li><a href="#acknowledgments">Acknowledgments</a></li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## About The Project


This project was born from a desire to create a space for developers and 
researchers where they could easily have access to large dialog datasets.


You will be able to find everything you need to download, extract and process 
the data.

This project is made possible thanks to the computer science laboratory of 
Grenoble (LIG) and the MIAI institute. Thanks to them for making this 
project possible

<p align="right">(<a href="#top">back to top</a>)</p>



### Built With

* [Python 3.7](https://www.python.org/downloads/)
* [Pip](https://pypi.org/project/pip/)
* [PushShift.io](https://pushshift.io/)

<p align="right">(<a href="#top">back to top</a>)</p>



<!-- GETTING STARTED -->
## Getting Started

To start using the project, you need to install some system dependencies

### Installation

1. Clone the repo
   ```sh
   git clone git@github.com:Torilen/French-Dialogue-Dataset.git
   ```
2. Got into it
   ```sh
   cd French-Dialogue-Dataset
   ```
3. Run installation script
   ```sh
   sh install.sh
   ```

<p align="right">(<a href="#top">back to top</a>)</p>



<!-- USAGE EXAMPLES -->
## Usage

### First Step : Data acquisition
   ```sh
   python getAndConcatData.py --help
usage: getAndConcatData.py [-h] [--languageThreshold LANGUAGETHRESHOLD]
                           [--decompressedSourceFilePath DECOMPRESSEDSOURCEFILEPATH]
                           [--listSubredditFilePath LISTSUBREDDITFILEPATH]
                           [--maxCommentProcessed MAXCOMMENTPROCESSED]
                           [--useSubredditFilter USESUBREDDITFILTER]
                           [--downloadData DOWNLOADDATA]
                           [--languageToExtract LANGUAGETOEXTRACT]

Acquisition et traitement des données

optional arguments:
  -h, --help            show this help message and exit
  --languageThreshold LANGUAGETHRESHOLD
                        Lowest ratio of language to non-language text. Enter a
                        value between 0 and 1.
  --decompressedSourceFilePath DECOMPRESSEDSOURCEFILEPATH
                        Path to the source file downloaded and decompressed by
                        download.sh
  --listSubredditFilePath LISTSUBREDDITFILEPATH
                        Path to the file contains the list of accepted
                        subreddit
  --maxCommentProcessed MAXCOMMENTPROCESSED
                        Maximum number of comment processed
  --useSubredditFilter USESUBREDDITFILTER
                        Use subreddit file ?
  --downloadData DOWNLOADDATA
                        The data source are already downloaded ?
  --languageToExtract LANGUAGETOEXTRACT
                        The language you want to extract from reddit ["fr",
                        "en", "es", etc]
   ```

Some commands example:
   ```sh
   python getAndConcatData.py --languageThreshold 0.5 --useSubredditFilter False --downloadData False --languageToExtract "fr"
   ```
   ```sh
   python getAndConcatData.py --languageThreshold 0.7 --useSubredditFilter True --languageToExtract "fr" --listSubredditFilePath "./data/acceptedSubbredit.txt"
   ```


<p align="right">(<a href="#top">back to top</a>)</p>

### Second Step : Data recomposition
```sh
python constructDialogueDataset.py --help
usage: constructDialogueDataset.py [-h]
                                   [--extractedPreprocessCsvFilePath EXTRACTEDPREPROCESSCSVFILEPATH]

Construction des données dialogues

optional arguments:
  -h, --help            show this help message and exit
  --extractedPreprocessCsvFilePath EXTRACTEDPREPROCESSCSVFILEPATH
                        Path to the source file preprocessed by
                        getAndConcatData.py
   ```
Example:
   ```sh
   python constructDialogueDataset.py --extractedPreprocessCsvFilePath "./reddit_source_fr_preprocessed.csv"
   ```
<!-- ROADMAP -->
## Roadmap

- [x] Multi-language Support
- [ ] Add some other data sources


<p align="right">(<a href="#top">back to top</a>)</p>


<!-- LICENSE -->
## License
<a rel="license" href="http://creativecommons.org/licenses/by-nc/3.0/fr/"><img alt="Licence Creative Commons" style="border-width:0" src="https://i.creativecommons.org/l/by-nc/3.0/fr/88x31.png" /></a><br />Ce(tte) œuvre est mise à disposition selon les termes de la <a rel="license" href="http://creativecommons.org/licenses/by-nc/3.0/fr/">Licence Creative Commons Attribution - Pas d’Utilisation Commerciale 3.0 France</a>.
Distributed under License. See `LICENSE.md` for more information.

<p align="right">(<a href="#top">back to top</a>)</p>



<!-- CONTACT -->
## Contact

[Ilyes Aniss Bentebib](https://ilyesbentebib.com) - aniss.bentebib@univ-grenoble-alpes.fr

Project Link: [https://github.com/Torilen/French-Dialogue-Dataset](https://github.com/Torilen/French-Dialogue-Dataset)

<p align="right">(<a href="#top">back to top</a>)</p>



<!-- ACKNOWLEDGMENTS -->
## Acknowledgments

* [LIG](https://choosealicense.com)
* [MIAI Institue](https://www.webpagefx.com/tools/emoji-cheat-sheet)
* [Jean-Pierre Chevallet](https://www.linkedin.com/in/jean-pierre-chevallet-8191255/)
* [Didier Schwab](https://www.linkedin.com/in/didierschwab/?originalSubdomain=fr)

<p align="right">(<a href="#top">back to top</a>)</p>



<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[contributors-shield]: https://img.shields.io/github/contributors/Torilen/French-Dialogue-Dataset.svg?style=for-the-badge
[contributors-url]: https://github.com/Torilen/French-Dialogue-Dataset/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/Torilen/French-Dialogue-Dataset.svg?style=for-the-badge
[forks-url]: https://github.com/Torilen/French-Dialogue-Dataset/network/members
[stars-shield]: https://img.shields.io/github/stars/Torilen/French-Dialogue-Dataset.svg?style=for-the-badge
[stars-url]: https://github.com/Torilen/French-Dialogue-Dataset/stargazers
[issues-shield]: https://img.shields.io/github/issues/Torilen/French-Dialogue-Dataset.svg?style=for-the-badge
[issues-url]: https://github.com/Torilen/French-Dialogue-Dataset/issues
[license-shield]: https://img.shields.io/github/license/Torilen/French-Dialogue-Dataset.svg?style=for-the-badge
[license-url]: https://github.com/Torilen/French-Dialogue-Dataset/blob/master/LICENSE.md
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555
[linkedin-url]: https://www.linkedin.com/in/aniss-bentebib-a449a8155/
[product-screenshot]: images/screenshot.png