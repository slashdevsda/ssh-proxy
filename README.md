
# Psychic Bear

SSH-Proxy using python3 and Paramiko

## Using a Virtualenv

### Setup & downloading

```
$ mkdir -p psychic-bear/venv && cd psychic-bear
$ virtualenv3 venv
$ source venv/bin/activate
$ git clone https://github.com/ecuer-thomas/ssh-proxy.git
$ cd ssh-proxy
$ pip install -r requierment.txt
```


### Run

```
$ cd psychic-bear/ssh-proxy
$ source ../venv/bin/activate
$ python -m "psychic_bear.psychic_bear"
```

## Using PIP

```
$ git clone https://github.com/ecuer-thomas/ssh-proxy.git
$ cd ssh-proxy && python setup.py install
$ psychic_bear
     ...
     ...
     ...
```

