/* TEMPLATE GENERATED TESTCASE FILE
Filename: CWE789_Uncontrolled_Mem_Alloc__random_ArrayList_66b.java
Label Definition File: CWE789_Uncontrolled_Mem_Alloc.int.label.xml
Template File: sources-sink-66b.tmpl.java
*/
/*
 * @description
 * CWE: 789 Uncontrolled Memory Allocation
 * BadSource: random Set data to a random value
 * GoodSource: A hardcoded non-zero, non-min, non-max, even number
 * Sinks: ArrayList
 *    BadSink : Create an ArrayList using data as the initial size
 * Flow Variant: 66 Data flow: data passed in an array from one method to another in different source files in the same package
 *
 * */






import java.util.ArrayList;

public class CWE789_Uncontrolled_Mem_Alloc__random_ArrayList_66b
{
    public void badSink(int dataArray[] ) throws Throwable
    {
        int data = dataArray[2];

        /* POTENTIAL FLAW: Create an ArrayList using data as the initial size.  data may be very large, creating memory issues */
        ArrayList intArrayList = new ArrayList(data);

    }

    /* goodG2B() - use goodsource and badsink */
    public void goodG2BSink(int dataArray[] ) throws Throwable
    {
        int data = dataArray[2];

        /* POTENTIAL FLAW: Create an ArrayList using data as the initial size.  data may be very large, creating memory issues */
        ArrayList intArrayList = new ArrayList(data);

    }
}
