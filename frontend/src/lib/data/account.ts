import api from "~/src/lib/data/api";
import { type AccountInfo } from "~/src/lib/definitions/account";

export async function getAccountDataFromAPI() {
  try {
    const response = await api.get<AccountInfo>('/account');

    if (response.status == 200) {
      return response.data;
    } else {
      return null;
    }
  } catch (error) {
    console.error(error);
    return null;
  }
}