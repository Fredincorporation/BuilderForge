/**
 * BuilderForge EIP-1193 Web3 Helper
 * 
 * Direct browser wallet integration for OKX Wallet & MetaMask.
 */

export interface Web3WalletState {
  connected: boolean;
  address: string;
  chainId: string;
  providerName: string;
}

/**
 * Get active Web3 provider (prefers OKX Wallet extension).
 */
export function getWeb3Provider(): any {
  if (typeof window === "undefined") return null;

  const win = window as any;
  if (win.okxwallet) {
    return win.okxwallet;
  }
  if (win.ethereum) {
    return win.ethereum;
  }
  return null;
}

/**
 * Connect to browser Web3 wallet.
 */
export async function connectWeb3Wallet(): Promise<Web3WalletState> {
  const provider = getWeb3Provider();
  if (!provider) {
    throw new Error("No Web3 wallet found. Please install the OKX Wallet or MetaMask extension.");
  }

  try {
    const accounts: string[] = await provider.request({
      method: "eth_requestAccounts",
    });

    if (!accounts || accounts.length === 0) {
      throw new Error("No accounts authorized by wallet.");
    }

    const chainId: string = await provider.request({
      method: "eth_chainId",
    });

    const isOKX = Boolean((window as any).okxwallet);

    return {
      connected: true,
      address: accounts[0],
      chainId: chainId || "0x41", // 0x41 = OKC Testnet
      providerName: isOKX ? "OKX Wallet" : "MetaMask / EIP-1193",
    };
  } catch (err: any) {
    throw new Error(err.message || "Failed to connect Web3 wallet");
  }
}

/**
 * Request transaction signature for contract deployment.
 */
export async function requestContractDeployTx(
  fromAddress: string,
  bytecode: string
): Promise<string> {
  const provider = getWeb3Provider();
  if (!provider) {
    throw new Error("Web3 provider not available");
  }

  try {
    const txHash: string = await provider.request({
      method: "eth_sendTransaction",
      params: [
        {
          from: fromAddress,
          data: bytecode.startsWith("0x") ? bytecode : `0x${bytecode}`,
          gas: "0x5208", // 21000 gas units
        },
      ],
    });

    return txHash;
  } catch (err: any) {
    throw new Error(err.message || "Transaction signature rejected by wallet");
  }
}
