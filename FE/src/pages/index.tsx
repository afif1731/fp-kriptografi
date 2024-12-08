import Layout from '@/components/layout/layout'

import { FormEvent, useState } from 'react'
import { Button, Card, Textarea, Select, Option, Dialog, DialogHeader, DialogBody } from '@material-tailwind/react'
import axios, { AxiosResponse } from 'axios'

import { BackendAPIResponse } from '@/components/assets/model'

import { IoCloseSharp } from 'react-icons/io5';
import { ImSpinner8 } from "react-icons/im";

interface IForm {
  message: string;
}

interface IResultNIST {
  name: string;
  elapsed_time: number;
  score: number;
  status: 'PASSED' | 'FAILED'
}

interface IAnalyzePRNG {
  dec_duration: string;
  decryption: string;
  enc_duration: string;
  encryption: number[];
  nist_test_result: IResultNIST[];
  original: string;
}

interface IResponse {
  status: 'success' | 'error' | 'closed';
  header: string;
  message: string;
}

const defaultResponse: IResponse = {
  status: 'closed',
  header: '',
  message: ''
}

export default function IndexPage() {
  const [message, setMessage] = useState<string | null>(null);
  const [loading, setLoading] = useState<boolean>(false);
  const [algorithm, setAlgorithm] = useState<'RCTM' | 'RK4' | 'Compare'>('RCTM');
  const [result1, setResult1] = useState<IAnalyzePRNG | null>(null);
  const [dialogOpen, setDialogOpen] = useState<boolean>(false);
  const [formResponse, setFormResponse] = useState<IResponse>(defaultResponse);
  
  const handleDialog = (res: IResponse) => {
      if(res.status === 'closed' || !res) setDialogOpen(false);
      else setDialogOpen(true);
      setFormResponse(res);
  };

  const defineNISTTestType = (input: string): string => {
    switch (input) {
      case 'Monobit':
        return 'Frequency (Monobit)';
      case 'Runs':
        return 'Run Test';
      case 'Longest Run Ones In A Block':
        return 'Longest Run of Ones in a Block';
      case 'Non Overlapping Template Matching':
        return 'Non-Overlapping Template Matching';
      case 'Cumulative Sums':
        return 'Cumulative Sums (Forwarded)';
      default:
        return input;
    }

  }

  async function handleSubmit(event: FormEvent) {
    try {
      event.preventDefault();

      const data: IForm = {
        message: message as string
      }

      setLoading(true);
      const result: AxiosResponse<BackendAPIResponse<IAnalyzePRNG>> = await axios.post(
        `${process.env.NEXT_PUBLIC_BE_URL || 'http://localhost:4000'}/${algorithm.toLowerCase()}`,
        data
      );

      if(result?.status == 200) {
        setLoading(false);
        setResult1(result.data.data as IAnalyzePRNG);
      } else {
        setLoading(false);
        handleDialog({
          status: 'error',
          header: 'failed to send your form',
          message: result.data?.message || ''
        });
      }
    } catch(error: any) {
      setLoading(false);
      handleDialog({
        status: 'error',
        header: 'failed to send your form',
        message: String(error)
      });
    }
  }

  return (
    <Layout title='Home'>
      <main>
        <div className='min-h-screen h-auto pt-5'>
          <div className='flex flex-col gap-3 items-center justify-center px-[5%]'>
            <h1 className='ptm-h2 text-black font-bold'>El-Gamal with CSPRNG</h1>
            <h5 className='ptm-h5 text-gray-800 font-medium'>El-Gamal Algorithm with Chaos-Based Pseudo Random Number Generator</h5>
          </div>

          <div className='flex flex-col gap-5 justify-center pt-10 md:px-[10%] px-[3%]'>
            <div className='px-[10%]'>
              <Card className='flex flex-col justify-center items-center'>
                <form className='mt-4 mb-2 flex flex-col w-full bg-white rounded-2xl p-5' onSubmit={handleSubmit}>
                  <p className='ptm-card-title text-black pb-3'>Input your Message</p>
                  <div className='mb-1 flex flex-col gap-3 text-black'>
                    <p className='ptm-p2 text-gray-900 font-medium'>Message</p>
                    <Textarea label='message' className='px-2' value={message as string} onChange={(e) => setMessage(e.target.value)} />
                    <p className='ptm-p2 text-gray-900 font-medium'>Algorithm</p>
                    <Select variant='outlined' label='Algorithm' value={algorithm} onChange={(val) => setAlgorithm(val as 'RCTM' | 'RK4' | 'Compare')}>
                      <Option value='RCTM'>Robust Chaotic Tent Map</Option>
                      <Option value='RK4'>Neural Network</Option>
                    </Select>
                    <Button className='flex mt-3 w-full' fullWidth type='submit'>
                      <span className='ptm-p2 font-bold w-full text-center text-white'>Submit</span>
                    </Button>
                  </div>
                </form>
              </Card>
            </div>

            <div className='flex flex-col justify-center pb-24'>
              {
                loading
                ?
                <div className='flex flex-row gap-3 justify-center items-center pt-3'>
                  <p className='ptm-p4 flex text-black font-semibold animate-spin'>Loading Data</p>
                  <ImSpinner8 className='animate-spin' />
                </div>
                :
                result1 === null
                ?
                <></>
                :
                <div className='flex flex-col w-full items-center'>
                  <h3 className='ptm-h3 text-black font-bold'>CSPRNG {algorithm} Result</h3>
                  <div className='flex flex-col w-full gap-5 justify-start pt-8'>
                    <h4 className='ptm-h4 text-black font-bold'>Encryption-Decryption Status</h4>
                    <table className=' w-full border-separate border-tools-table-outline border-black border-2 rounded-t-xl'>
                      <thead className='ptm-h5 rounded-t text-white'>
                        <th className='bg-deep-orange-700 rounded-tl-xl w-[35%]'>Item</th>
                        <th className='bg-deep-orange-700 rounded-tr-xl w-[65%]'>Value</th>
                      </thead>
                      <tbody className=' bg-white'>
                        <tr className='border-black border-2'>
                          <th className='bg-blue-gray-50 ptm-p4 text-black font-semibold'>Encrypt Duration</th>
                          <th className='bg-blue-gray-50 ptm-p4 text-black font-semibold'>{result1.enc_duration} Second</th>
                        </tr>
                        <tr className='border-black border-2'>
                          <th className='bg-blue-gray-50 ptm-p4 text-black font-semibold'>Decrypt Duration</th>
                          <th className='bg-blue-gray-50 ptm-p4 text-black font-semibold'>{result1.dec_duration} Second</th>
                        </tr>
                        <tr className='border-black border-2'>
                          <th className='bg-blue-gray-50 ptm-p4 text-black font-semibold'>Cipher Text</th>
                          <th className='bg-blue-gray-50 ptm-p4 text-black font-semibold'>{`${result1.encryption[0]}, ${result1.encryption[1]}`}</th>
                        </tr>
                        <tr className='border-black border-2'>
                          <th className='bg-blue-gray-50 ptm-p4 text-black font-semibold'>Decryption Result</th>
                          <th className='bg-blue-gray-50 ptm-p4 text-black font-semibold'>{result1.decryption}</th>
                        </tr>
                        <tr className='border-black border-2'>
                          <th className='bg-blue-gray-50 ptm-p4 text-black font-semibold'>Status</th>
                          {
                            result1.decryption === result1.original
                            ?
                            <th className='bg-blue-gray-50 ptm-p4 text-green-500 font-semibold'>Success</th>
                            :
                            <th className='bg-blue-gray-50 ptm-p4 text-red-500 font-semibold'>Failed</th>
                          }
                        </tr>
                      </tbody>
                    </table>

                    <h4 className='ptm-h4 text-black font-bold pt-5'>NIST SP 800-22 Test Result</h4>
                    <table className=' w-full border-separate border-tools-table-outline border-black border-2 rounded-t-xl'>
                      <thead className='ptm-h5 rounded-t text-white'>
                        <th className='bg-blue-gray-800 rounded-tl-xl w-[45%]'>Test Type</th>
                        <th className='bg-blue-gray-800 w-[10%]'>P-Value</th>
                        <th className='bg-blue-gray-800 w-[25%]'>Elapsed Time (ms)</th>
                        <th className='bg-blue-gray-800 rounded-tr-xl w-[20%]'>Status</th>
                      </thead>
                      <tbody className=' bg-white'>
                        {
                          result1.nist_test_result.map((item) => (
                            <tr key={item.name} className='border-black border-2'>
                              <th className='bg-blue-gray-50 ptm-p4 text-black text-start font-semibold'>{defineNISTTestType(item.name)}</th>
                              <th className='bg-blue-gray-50 ptm-card-btn text-black font-semibold'>{item.score}</th>
                              <th className='bg-blue-gray-50 ptm-card-btn text-black font-semibold'>{item.elapsed_time}</th>
                              <th className='bg-blue-gray-50'>
                                {
                                  item.status === 'PASSED'
                                  ?
                                  <span className=' bg-green-900 text-white font-bold ptm-p5 py-1 px-5 rounded-full'>PASSED</span>
                                  :
                                  <span className=' bg-red-900 text-white font-bold ptm-p5 py-1 px-5 rounded-full'>FAILED</span>
                                }
                              </th>

                            </tr>
                          ))
                        }
                      </tbody>
                    </table>
                  </div>
                </div>
              }
            </div>
          </div>

          <div>
            <Dialog
                open= {dialogOpen}
                size='lg'
                handler={handleDialog}
                className=' bg-white min-h-[40vh] rounded-2xl'
            >
                <div className='h-full min-h-[40vh] items-start rounded-2xl px-8'>
                    <div className='flex flex-row justify-between items-start'>
                        <DialogHeader className='flex text-black w-[80%]'>
                            <p className='lg:ptm-h2 ptm-h4'>
                                {
                                    formResponse.header
                                }
                            </p>
                        </DialogHeader>
                        <button onClick={() => handleDialog(defaultResponse)} className='p-5'>
                            <IoCloseSharp className=' text-black size-16' />
                        </button>
                    </div>
                    <DialogBody className=' text-black text-left'>
                        <p className='ptm-p4'>
                            {
                                formResponse.message
                            }
                        </p>
                    </DialogBody>
                </div>
            </Dialog>
          </div>
        </div>
      </main>
    </Layout>
  )
}
