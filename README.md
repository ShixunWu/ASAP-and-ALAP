<h1 align="center">
  ASAP-and-ALAP for DAG
</h1>
<h4 align="center">Get priority for one directed acyclic graphs(DAG) by appling ASAP or ALAP Scheduling Algorithm.</h4>
<p align="center">
  </a>
    <img src="https://img.shields.io/badge/Python-3.7+-brightgreen">

</p>
<p align="center">
  <a href="#-dependencies-and-required-packages">Dependencies</a> •
  <a href="#%EF%B8%8F-usage">Usage</a> •
  <a href="#-features">Features</a> •
  <a href="#-limitations">Limitations</a>
</p>

## 📦 Required Packages

Assuming that `Python3` is installed in the targeted machine, to install the required packages:

```
pip install networkx
```

## ⚙️ Usage

#### Task generator:

The options of the ASAP-and-ALAP are as follows (`python3 asap_alap.py -h`):

```
usage: asap_alap.py [-h] [-s | -l] DAGfile

Compute the priority for one directed acyclic graphs(DAG) by using ASAP or ALAP Scheduling Algorithm. (To test the program you can run the demo DAG file by 'python3 asap_alap.py -s ./DAG\
example/Tasks_1_Run_0.csv')

positional arguments:
  DAGfile     The DAG file path

optional arguments:
  -h, --help  show this help message and exit
  -s, --ASAP  Run ASAP scheduling algorithm
  -l, --ALAP  Run ALAP scheduling algorithm
```

To test the tool and run the asap with:

```
$ python3 asap_alap.py -s ./DAG\ example/Tasks_1_Run_0.csv'
```

#### DAG file format

The format infromation is in DAG example file. It helps you construct your DAG file.

## 🚧 Limitations

- Software is not fully tested
- There is no function to write priority back to the Tasks_1_Run_*.csv for the time being

## 🌱 Contribution

Feedback contributions are welcome

- Open pull request with improvements
- Discuss feedbacks and bugs in issues
