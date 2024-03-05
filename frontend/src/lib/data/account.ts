import api from "~/src/lib/data/api";

export interface AccountData {
  _User__id: string;
  _User__name: string;
  _User__email: string;
  _User__hashed_password: string;
  _User__my_progresses: any[];
  _User__latest_progress: null | any;
};

export async function getAccountDataFromAPI() {
  try {
    const response = await api.get<AccountData>('/account');

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