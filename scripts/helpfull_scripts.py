from brownie import accounts, config, network
from brownie.network import account
import eth_utils


# NON_FORKED_LOCAL_BLOCKCHAIN_ENVIRONMENTS = [
#    "hardhat", "development", "ganache"]
# LOCAL_BLOCKCHAIN_ENVIRONMENTS = NON_FORKED_LOCAL_BLOCKCHAIN_ENVIRONMENTS + [
#    "mainnet-fork-dev",
#    "binance-fork",
#   "matic-fork",
# ]

LOCAL_BLOCKCHAIN_ENVIRONMENTS = [
    "mainnet-fork-dev", "ganach-cli", "development"]
# def get_account(number=None):
#   if number:
#      return accounts[number]
# if network.show_active() in config["networks"]:
#    account = accounts.add(config["wallets"]["from_key"])
# if network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
#    return account[0]
# return None


def get_account(index=None, id=None):
    if index:
        return accounts[index]
    if network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        return accounts[0]
    if id:
        return accounts.load(id)
    if network.show_active() in config["networks"]:
        return accounts.add(config["wallets"]["from_key"])
    return None


def encode_function_data(initializer=None, *args):
    if len(args) == 0 or not initializer:
        return eth_utils.to_bytes(hexstr="0x")
    return initializer.encode_input(*args)


def upgrade(
    account,
    proxy,
    new_implementation_address,
    proxy_admin_contract=None,
    intializer=None,
    *args
):
    transaction = None
    if proxy_admin_contract:
        if intializer:
            encoded_function_call = encode_function_data(intializer, *args)
            transaction = proxy_admin_contract.upgradeAndCall(
                proxy.address,
                new_implementation_address,
                encode_function_data,
                {"from": account}
            )
        else:
            transaction = proxy_admin_contract.upgrade(
                proxy.address,
                new_implementation_address,
                {"from": account}
            )
    else:
        if intializer:
            encoded_function_call = encode_function_data(intializer, *args)
            transaction = proxy.upgradeToAndCall(
                new_implementation_address,
                encoded_function_call,
                {"from": account}
            )
        else:
            transaction = proxy.upgradeTo(
                new_implementation_address,
                {"from": account}
            )
    return transaction
