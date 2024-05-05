//
// Copyright (c) ZeroC, Inc. All rights reserved.
//
//
// Ice version 3.7.10
//
// <auto-generated>
//
// Generated from file `calculator.ice'
//
// Warning: do not edit this file.
//
// </auto-generated>
//

package Demo;

/**
 * Helper class for marshaling/unmarshaling GradeSeq.
 **/
public final class GradeSeqHelper
{
    public static void write(com.zeroc.Ice.OutputStream ostr, Grade[] v)
    {
        if(v == null)
        {
            ostr.writeSize(0);
        }
        else
        {
            ostr.writeSize(v.length);
            for(int i0 = 0; i0 < v.length; i0++)
            {
                Grade.ice_write(ostr, v[i0]);
            }
        }
    }

    public static Grade[] read(com.zeroc.Ice.InputStream istr)
    {
        final Grade[] v;
        final int len0 = istr.readAndCheckSeqSize(5);
        v = new Grade[len0];
        for(int i0 = 0; i0 < len0; i0++)
        {
            v[i0] = Grade.ice_read(istr);
        }
        return v;
    }

    public static void write(com.zeroc.Ice.OutputStream ostr, int tag, java.util.Optional<Grade[]> v)
    {
        if(v != null && v.isPresent())
        {
            write(ostr, tag, v.get());
        }
    }

    public static void write(com.zeroc.Ice.OutputStream ostr, int tag, Grade[] v)
    {
        if(ostr.writeOptional(tag, com.zeroc.Ice.OptionalFormat.FSize))
        {
            int pos = ostr.startSize();
            GradeSeqHelper.write(ostr, v);
            ostr.endSize(pos);
        }
    }

    public static java.util.Optional<Grade[]> read(com.zeroc.Ice.InputStream istr, int tag)
    {
        if(istr.readOptional(tag, com.zeroc.Ice.OptionalFormat.FSize))
        {
            istr.skip(4);
            Grade[] v;
            v = GradeSeqHelper.read(istr);
            return java.util.Optional.of(v);
        }
        else
        {
            return java.util.Optional.empty();
        }
    }
}
